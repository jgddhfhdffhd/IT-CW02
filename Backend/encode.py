from urllib.parse import quote_plus

username = "seeker"
password = "LoOhG4lri4s43MQo"  # 如果包含特殊字符，确保使用 URL 编码
encoded_password = quote_plus(password)

MONGO_URI = f"mongodb+srv://{username}:{encoded_password}@cluster0.xwiqe.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

print(MONGO_URI)