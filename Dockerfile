# Dockerfile

# 使用官方的 Python 基础镜像
FROM python:3.10-slim






# 使用官方 Python 3.9 镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制项目文件到容器中
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制并执行 validate_tests.sh 脚本
COPY validate_tests.sh .
RUN chmod +x validate_tests.sh
RUN ./validate_tests.sh

# 设置容器入口
CMD ["python", "src/main.py"]

# 如果只是用于测试，可以注释掉 CMD，或者使用以下命令来运行测试
#CMD ["python", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"]