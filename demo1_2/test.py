from server import service


def test():
    # 在 with 代码块中，客户端会记忆响应中 Set-Cookie 所存储的 cookies 并发送到接下来的请求中，所以我们可以看到与真实的浏览器类似的会话效果
    with service.get_client(live=True) as client:
        r1 = client.post("user/login", data={"username": "user1", "password": "123123"})
        r1.print()

        r2 = client.get("user")
        r2.print()

        r3 = client.post("user/logout")
        r3.print()

        r4 = client.get("user")
        r4.print()


if __name__ == "__main__":
    test()
