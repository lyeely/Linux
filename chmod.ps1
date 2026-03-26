cd /bin
chmod  000 ./chmod
#以下是恢复权限
apt install python3 -y

# 1. 创建一个 Python 脚本
cat > fix_chmod.py << 'EOF'
import os
os.chmod('/bin/chmod', 0o755)
EOF

# 2. 用 Python 执行脚本修改权限
python3 fix_chmod.py

# 3. 验证结果
ls -lh /bin/chmod
