"""API测试脚本"""
import requests
import json
from typing import Dict, Any


class APITester:
    """API测试器"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.api_v1 = f"{base_url}/api/v1"
        self.token = None
        self.test_results = []
    
    def log_test(self, name: str, success: bool, message: str = ""):
        """记录测试结果"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = f"{status} - {name}"
        if message:
            result += f": {message}"
        print(result)
        self.test_results.append({
            "name": name,
            "success": success,
            "message": message
        })
    
    def test_health(self):
        """测试健康检查"""
        try:
            response = requests.get(f"{self.base_url}/health")
            success = response.status_code == 200 and response.json()["status"] == "healthy"
            self.log_test("健康检查", success)
            return success
        except Exception as e:
            self.log_test("健康检查", False, str(e))
            return False
    
    def test_root(self):
        """测试根路径"""
        try:
            response = requests.get(f"{self.base_url}/")
            data = response.json()
            success = response.status_code == 200 and "version" in data
            self.log_test("根路径", success, f"Version: {data.get('version')}")
            return success
        except Exception as e:
            self.log_test("根路径", False, str(e))
            return False
    
    def test_login(self):
        """测试登录"""
        try:
            response = requests.post(
                f"{self.api_v1}/auth/login",
                json={
                    "email": "demo@example.com",
                    "password": "demo123"
                }
            )
            data = response.json()
            
            if data.get("success") and "token" in data.get("data", {}):
                self.token = data["data"]["token"]
                self.log_test("用户登录", True, f"User: {data['data']['user']['email']}")
                return True
            else:
                self.log_test("用户登录", False, data.get("error", {}).get("message", "Unknown error"))
                return False
        except Exception as e:
            self.log_test("用户登录", False, str(e))
            return False
    
    def test_dashboard_stats(self):
        """测试仪表板统计"""
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{self.api_v1}/dashboard/stats", headers=headers)
            data = response.json()
            
            success = data.get("success") and "stats" in data.get("data", {})
            stats_count = len(data.get("data", {}).get("stats", []))
            self.log_test("仪表板统计", success, f"Stats count: {stats_count}")
            return success
        except Exception as e:
            self.log_test("仪表板统计", False, str(e))
            return False
    
    def test_dashboard_projects(self):
        """测试项目列表"""
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(
                f"{self.api_v1}/dashboard/projects?page=1&limit=10",
                headers=headers
            )
            data = response.json()
            
            success = data.get("success") and "projects" in data.get("data", {})
            total = data.get("data", {}).get("total", 0)
            self.log_test("项目列表", success, f"Total projects: {total}")
            return success
        except Exception as e:
            self.log_test("项目列表", False, str(e))
            return False
    
    def test_knowledge_items(self):
        """测试知识库列表"""
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(
                f"{self.api_v1}/knowledge/items?page=1&limit=10",
                headers=headers
            )
            data = response.json()
            
            success = data.get("success") and "items" in data.get("data", {})
            items_count = len(data.get("data", {}).get("items", []))
            self.log_test("知识库列表", success, f"Items count: {items_count}")
            return success
        except Exception as e:
            self.log_test("知识库列表", False, str(e))
            return False
    
    def test_user_profile(self):
        """测试用户信息"""
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{self.api_v1}/user/profile", headers=headers)
            data = response.json()
            
            success = data.get("success") and "id" in data.get("data", {})
            user_id = data.get("data", {}).get("id", "")
            self.log_test("用户信息", success, f"User ID: {user_id}")
            return success
        except Exception as e:
            self.log_test("用户信息", False, str(e))
            return False
    
    def test_user_quota(self):
        """测试用户配额"""
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(f"{self.api_v1}/user/quota", headers=headers)
            data = response.json()
            
            success = data.get("success") and "plan" in data.get("data", {})
            plan = data.get("data", {}).get("plan", "")
            self.log_test("用户配额", success, f"Plan: {plan}")
            return success
        except Exception as e:
            self.log_test("用户配额", False, str(e))
            return False
    
    def test_terminology(self):
        """测试术语查询"""
        try:
            response = requests.get(f"{self.base_url}/v1/terminology/shots")
            data = response.json()
            
            success = data.get("status") == "success"
            self.log_test("术语查询", success)
            return success
        except Exception as e:
            self.log_test("术语查询", False, str(e))
            return False
    
    def test_analysis_create(self):
        """测试创建分析（不需要认证）"""
        try:
            response = requests.post(
                f"{self.api_v1}/analysis/create",
                json={
                    "url": "https://example.com/test.mp4",
                    "platform": "auto"
                }
            )
            data = response.json()
            
            success = data.get("success") and "analysisId" in data.get("data", {})
            analysis_id = data.get("data", {}).get("analysisId", "")
            self.log_test("创建分析", success, f"Analysis ID: {analysis_id}")
            return success
        except Exception as e:
            self.log_test("创建分析", False, str(e))
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "="*60)
        print("🚀 开始API测试")
        print("="*60 + "\n")
        
        print("📋 基础测试")
        print("-" * 60)
        self.test_health()
        self.test_root()
        print()
        
        print("🔐 认证测试")
        print("-" * 60)
        if not self.test_login():
            print("\n⚠️  登录失败，跳过需要认证的测试\n")
            return
        print()
        
        print("📊 仪表板测试")
        print("-" * 60)
        self.test_dashboard_stats()
        self.test_dashboard_projects()
        print()
        
        print("📚 知识库测试")
        print("-" * 60)
        self.test_knowledge_items()
        print()
        
        print("👤 用户管理测试")
        print("-" * 60)
        self.test_user_profile()
        self.test_user_quota()
        print()
        
        print("📖 术语测试")
        print("-" * 60)
        self.test_terminology()
        print()
        
        print("🎬 视频分析测试")
        print("-" * 60)
        self.test_analysis_create()
        print()
        
        # 统计结果
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r["success"])
        failed = total - passed
        
        print("="*60)
        print(f"📈 测试结果: {passed}/{total} 通过")
        if failed > 0:
            print(f"❌ {failed} 个测试失败")
            print("\n失败的测试:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['name']}: {result['message']}")
        else:
            print("✅ 所有测试通过!")
        print("="*60 + "\n")


if __name__ == "__main__":
    tester = APITester()
    tester.run_all_tests()

