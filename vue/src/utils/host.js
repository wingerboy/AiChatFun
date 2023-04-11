const apiHostMap = {
  qa: "http://localhost:7000",
  prod: "http://43.153.81.198:8000",
  online: "http://43.153.81.198",
};

export default apiHostMap["online"]; // 本地测试/线上部署：qa/online
