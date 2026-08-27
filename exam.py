import sys

books = []
next_id = 1

def load_books_from_file(filename="book.txt"):
    global next_id

    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f" {filename} 不存在。")
        return
    except Exception as e:
        print(e)
        return

    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split(",")
        if len(parts) != 3:
            print(f"跳过格式错误的行：{line}")
            continue
        title = parts[0].strip()
        try:
            price = float(parts[1].strip())
        except ValueError:
            print(f"价格格式错误，跳过该行：{line}")
            continue
        rented_str = parts[2].strip()
        rented = rented_str == "是"
        book = {
            "id": next_id,
            "title": title,
            "price": price,
            "rented": rented
        }
        books.append(book)
        next_id += 1

def add_info():
    global next_id
    print("\n--- 添加书籍 ---")
    title = input("请输入书名：").strip()
    if not title:
        print("书名不能为空！")
        return

    price_input = input("请输入价格（默认为0）：").strip()
    if price_input == "":
        price = 0.0
    else:
        try:
            price = float(price_input)
        except ValueError:
            print("价格格式错误，已设置为0。")
            price = 0.0

    rent_input = input("书籍是否已出租？（是/否，默认为否）：").strip()
    if rent_input == "是":
        rented = True
    else:
        rented = False

    book = {
        "id": next_id,
        "title": title,
        "price": price,
        "rented": rented
    }
    books.append(book)
    print(f"书籍《{title}》添加成功，编号为 {next_id}。")
    next_id += 1


def delete_info():
    print("\n--- 删除书籍 ---")
    try:
        book_id = int(input("请输入要删除的书籍编号："))
    except ValueError:
        print("编号必须是整数！")
        return

    found_book = None
    for book in books:
        if book["id"] == book_id:
            found_book = book
            break

    if found_book is None:
        print(f"编号 {book_id} 的书籍不存在。")
        return

    if found_book["rented"]:
        print("书籍已出租，暂无法删除。")
    else:
        books.remove(found_book)
        print(f"书籍《{found_book['title']}》（编号 {book_id}）已删除。")


def update_info():

    print("\n--- 修改书籍信息 ---")
    try:
        book_id = int(input("请输入要修改的书籍编号："))
    except ValueError:
        print("编号必须是整数！")
        return

    target_book = None
    for book in books:
        if book["id"] == book_id:
            target_book = book
            break

    if target_book is None:
        print(f"编号 {book_id} 的书籍不存在。")
        return

    print("可选修改字段：1.书名  2.价格  3.出租状态")
    choice = input("请输入要修改的字段编号（1/2/3）：").strip()
    if choice == "1":
        new_title = input("请输入新的书名：").strip()
        if new_title:
            target_book["title"] = new_title
            print("书名修改成功。")
        else:
            print("书名不能为空，未修改。")
    elif choice == "2":
        try:
            new_price = float(input("请输入新的价格："))
            target_book["price"] = new_price
            print("价格修改成功。")
        except ValueError:
            print("价格格式错误，未修改。")
    elif choice == "3":
        new_rent = input("请输入新的出租状态（是/否）：").strip()
        if new_rent == "是":
            target_book["rented"] = True
            print("出租状态已改为「已出租」。")
        elif new_rent == "否":
            target_book["rented"] = False
            print("出租状态已改为「未出租」。")
        else:
            print("输入无效，未修改。")
    else:
        print("无效的选择。")


def search_info():
    """根据书名查询书籍信息，使用占位符格式化输出"""
    print("\n--- 查询单个书籍 ---")
    keyword = input("请输入要查询的书名（支持模糊匹配）：").strip()
    if not keyword:
        print("查询关键字不能为空。")
        return

    # 模糊匹配：书名中包含关键字
    matched = [book for book in books if keyword in book["title"]]
    if not matched:
        print(f"未找到书名包含「{keyword}」的书籍。")
        return

    print(f"\n共找到 {len(matched)} 本相关书籍：")
    for book in matched:

        print("编号：{:<5} 书名：{:<20} 价格：{:<8.2f} 出租状态：{}".format(
            book["id"], book["title"], book["price"],
            "是" if book["rented"] else "否"
        ))

def search_all():
    """输出所有书籍的信息"""
    print("\n--- 所有书籍列表 ---")
    if not books:
        print("当前没有任何书籍。")
        return

    for book in books:
        print("编号：{:<5} 书名：{:<20} 价格：{:<8.2f} 出租状态：{}".format(
            book["id"], book["title"], book["price"],
            "是" if book["rented"] else "否"
        ))


def print_info():
    """打印操作菜单"""
    print("\n" + "=" * 45)
    print("          图书租借管理系统")
    print("=" * 45)
    print("① 输入1: 添加书籍(书籍编号, 书籍名, 书籍价格, 书籍出租状态【是/否】)")
    print("② 输入2: 删除书籍(根据编号删除)")
    print("   【删除时，需要判断书籍出租状态，如果书籍未出租，则删除书籍；如果书籍已出租，则打印“书籍已出租，暂无法删除”】")
    print("③ 输入3: 修改书籍信息(只能改书籍名, 书籍出租状态)")
    print("④ 输入4: 查询单个书籍信息(根据书籍名查)")
    print("⑤ 输入5: 查询所有书籍信息")
    print("⑥ 输入6: 退出系统")
    print("=" * 45)


def login():
    ADMIN_USER = "admin"
    ADMIN_PASS = "admin123"

    print("欢迎使用图书租借管理系统")
    for attempt in range(1, 4):
        username = input("请输入用户名：").strip()
        password = input("请输入密码：").strip()
        if username == ADMIN_USER and password == ADMIN_PASS:
            print("登陆成功！")
            return True
        else:
            remaining = 3 - attempt
            if remaining > 0:
                print(f"账号或密码错误，请重试（剩余 {remaining} 次机会）")
            else:
                print("错误次数达上限，系统退出。")
                sys.exit(0)
    return False


if __name__ == "__main__":
    load_books_from_file("book.txt")
    
    login()

    while True:
        print_info()
        choice = input("请输入您的选择（1-6）：").strip()
        # 处理非法输入
        if choice not in ("1", "2", "3", "4", "5", "6"):
            print("无效输入，请输入1-6之间的数字。")
            continue

        if choice == "1":
            add_info()
        elif choice == "2":
            delete_info()
        elif choice == "3":
            update_info()
        elif choice == "4":
            search_info()
        elif choice == "5":
            search_all()
        elif choice == "6":
            print("感谢使用图书租借管理系统，再见！")
            break