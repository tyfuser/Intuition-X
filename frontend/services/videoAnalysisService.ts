import axios, { AxiosInstance } from 'axios';
import { JobResponse, AnalysisOptions, VideoSource, HistoryItem } from '../types';

// 镜头拆解分析功能使用独立的 API 地址
const SHOT_ANALYSIS_BASE_URL = import.meta.env.VITE_SHOT_ANALYSIS_BASE_URL || 'http://localhost:8000';
const API_BASE_PATH = '/v1/video-analysis';

// 创建独立的 Axios 实例
const shotAnalysisApi: AxiosInstance = axios.create({
  baseURL: SHOT_ANALYSIS_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * 创建视频分析任务
 */
export const createAnalysisJob = async (
  videoSource: VideoSource,
  options: AnalysisOptions = {}
): Promise<JobResponse> => {
  const requestBody = {
    mode: 'learn',
    target_video: {
      source: videoSource
    },
    options: {
      frame_extract: {
        fps: options.frame_extract?.fps || 2.0,
        max_frames: options.frame_extract?.max_frames || 240
      },
      llm: {
        provider: options.llm?.provider || 'sophnet',
        enabled_modules: options.llm?.enabled_modules || [
          'camera_motion',
          'lighting',
          'color_grading'
        ]
      }
    }
  };

  try {
    const response = await shotAnalysisApi.post<JobResponse>(`${API_BASE_PATH}/jobs`, requestBody);
    return response.data;
  } catch (error) {
    console.error('创建分析任务失败:', error);
    throw error;
  }
};

/**
 * 查询任务状态
 */
export const getJobStatus = async (jobId: string): Promise<JobResponse> => {
  try {
    const response = await shotAnalysisApi.get<JobResponse>(`${API_BASE_PATH}/jobs/${jobId}`);
    return response.data;
  } catch (error) {
    console.error('查询任务状态失败:', error);
    throw error;
  }
};

/**
 * 轮询任务状态直到完成（已弃用，使用 streamJobProgress 代替）
 */
export const pollJobStatus = async (
  jobId: string,
  onProgress?: (progress: JobResponse) => void,
  maxAttempts: number = 120,
  interval: number = 1000
): Promise<JobResponse> => {
  let attempts = 0;

  while (attempts < maxAttempts) {
    try {
      const data = await getJobStatus(jobId);

      // 调用进度回调
      if (onProgress) {
        onProgress(data);
      }

      // 检查任务状态
      if (data.status === 'succeeded') {
        return data;
      } else if (data.status === 'failed') {
        throw new Error(data.error?.message || '分析任务失败');
      }

      // 等待后继续轮询
      await sleep(interval);
      attempts++;
    } catch (error) {
      console.error('轮询任务状态失败:', error);
      throw error;
    }
  }

  throw new Error('分析超时，请稍后查看历史记录');
};

/**
 * SSE 流式接收任务进度和片段数据
 */
export const streamJobProgress = (
  jobId: string,
  callbacks: {
    onProgress?: (percent: number, message: string, stage?: string) => void;
    onSegments?: (segments: any[]) => void;
    onComplete?: (result: any) => void;
    onError?: (error: string) => void;
  }
): { close: () => void } => {
  const url = `${SHOT_ANALYSIS_BASE_URL}${API_BASE_PATH}/jobs/${jobId}/stream`;
  const eventSource = new EventSource(url);

  eventSource.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);

      switch (data.type) {
        case 'progress':
          // 进度更新
          if (callbacks.onProgress && data.progress) {
            callbacks.onProgress(
              data.progress.percent || 0,
              data.progress.message || '',
              data.progress.stage
            );
          }
          break;

        case 'segments':
          // 片段数据更新
          if (callbacks.onSegments && data.segments) {
            callbacks.onSegments(data.segments);
          }
          break;

        case 'complete':
          // 任务完成
          if (callbacks.onComplete && data.result) {
            callbacks.onComplete(data.result);
          }
          eventSource.close();
          break;

        case 'error':
          // 错误
          if (callbacks.onError) {
            callbacks.onError(data.error?.message || '未知错误');
          }
          eventSource.close();
          break;
      }
    } catch (error) {
      console.error('解析 SSE 数据失败:', error);
    }
  };

  eventSource.addEventListener('done', () => {
    console.log('SSE 流结束');
    eventSource.close();
  });

  eventSource.addEventListener('error', (event) => {
    console.error('SSE 连接错误:', event);
    if (callbacks.onError) {
      callbacks.onError('连接中断');
    }
    eventSource.close();
  });

  eventSource.onerror = (error) => {
    console.error('SSE 错误:', error);
    eventSource.close();
  };

  return {
    close: () => eventSource.close()
  };
};

/**
 * 获取历史记录
 */
export const getHistory = async (limit: number = 50): Promise<HistoryItem[]> => {
  try {
    const response = await shotAnalysisApi.get<HistoryItem[]>(`${API_BASE_PATH}/history`, {
      params: { limit }
    });
    return response.data;
  } catch (error) {
    console.error('获取历史记录失败:', error);
    throw error;
  }
};

/**
 * 删除任务
 */
export const deleteJob = async (jobId: string): Promise<void> => {
  try {
    await shotAnalysisApi.delete(`${API_BASE_PATH}/jobs/${jobId}`);
  } catch (error) {
    console.error('删除任务失败:', error);
    throw error;
  }
};

/**
 * 工具函数：延迟
 */
function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

