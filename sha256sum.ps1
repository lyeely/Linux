# 创建一个文件
echo "这是要发布的文件内容" > my_release_file.txt

# 生成校验文件
sha256sum my_release_file.txt > my_release_file.txt.sha256

cat my_release_file.txt.
复制内容到记事本并保存

cat my_release_file.txt.sha256
#复制内容并保存为原名文件
