import queue

mark = 1
layer_mark = 0
code = []
num_table = 4
code_len = num_table * 3


class TreeNode:
    """
        树节点定义，left、right分别为左右孩子
    """

    def __init__(self, val=None, left=None, right=None, layer=None, left_val=None, right_val=None):
        self.val = val
        self.left = left
        self.right = right
        self.layer = layer
        self.left_val = left_val
        self.right_val = right_val


def visit(treenode):
    print(str(treenode.val), end=' ')


'''
递归深度优先遍历——前序遍历
'''


def RecursionPreOrder(root):
    if root is not None:
        visit(root)
        RecursionPreOrder(root.left)
        RecursionPreOrder(root.right)


def lr_tag(root):
    """
    采用先根遍历进行左右值编码
    :param root: 待左右值编码树根
    :return: None,对树左右值编码
    """
    global mark
    if root is None:
        return
    else:
        root.left_val = mark
        mark += 1
        lr_tag(root.left)
        lr_tag(root.right)
        root.right_val = mark
        mark += 1


def layer_tag(root):
    """
    采用先根遍历进行层序编码
    :param root: 层序编码树根
    :return: None，对树层序编码
    """
    global layer_mark
    if root is not None:
        root.layer = layer_mark
        layer_mark += 1
        layer_tag(root.left)
        layer_tag(root.right)
        layer_mark -= 1


'''
递归深度优先遍历——中序遍历
'''


def RecursionInOrder(root):
    if root is not None:
        RecursionInOrder(root.left)
        visit(root)
        RecursionInOrder(root.right)


'''
递归深度优先遍历——后序遍历
'''


def get_coding(root):
    """
    对编码后的二叉树获取编码，采用后序遍历
    :param root: 编码后树根
    :return:
    """
    if root is not None:
        get_coding(root.left)
        get_coding(root.right)
        if root.left is None and root.right is None:
            start = (ord(root.val) - ord("A")) * 3
            code[start: start + 3] = [root.left_val, root.right_val, root.layer]


def encoding(root):
    global layer_mark, mark, code
    lr_tag(root)
    mark = 1
    layer_tag(root)
    layer_mark = 0
    code = [0] * code_len
    get_coding(root)


def tree_construct(expr):
    """

    :param expr:表示join顺序的括号表达式
    :return:root，所有join树树根，包括中间产物
    """
    tree_list = []
    op_stack = []  # list simulate stack
    tab_que = queue.Queue()
    tree_que = queue.Queue()
    for c in expr:
        if c == "(":
            op_stack.append(c)
        elif c == ")":
            op_stack.pop()
            if tab_que.qsize() != 0:  # 表做join
                t1 = tab_que.get()
                if tab_que.qsize() == 0:  # 表和字数做join
                    tree = tree_que.get()
                    node = TreeNode(t1)
                    link = TreeNode("x")
                    link.left = tree
                    link.right = node
                    tree_que.put(link)
                    tree_list.append(link)
                else:
                    t2 = tab_que.get()
                    node1 = TreeNode(t1)
                    node2 = TreeNode(t2)
                    link = TreeNode("x")
                    link.left = node1
                    link.right = node2
                    tree_list.append(link)
                    tree_que.put(link)
            else:  # 子树做join
                tree1 = tree_que.get()
                tree2 = tree_que.get()
                link = TreeNode("x")
                link.left = tree1
                link.right = tree2
                tree_que.put(link)
                tree_list.append(link)
        else:
            tab_que.put(c)
    return tree_list


def encode(expr):
    """

    :param expr: join顺序的括号表达式
    :return: None, 对join树包括中间子树的左右值编码 dim = (表个数*3),编码存储至codes: list中
    """
    global code_len
    join_trees = tree_construct(expr)
    codes = []
    global code
    for t in join_trees:
        encoding(t)
        # if len(code) < code_len:
        #     code = code + [0] * (code_len - len(code))
        codes.append(code)
    return codes


def generate_exprs(tables):
    """

    :param tables: str, exp: "stu teacher eply admin user"
    :return: exprs:list 所有可能join情况的列表
    """
    global num_table
    table_list = tables.split(" ")
    num_table = len(table_list)  # 默认从A开始生成num个表的别称


def transition(state, action):
    """

    :param state: 当前状态编码
    :param action: 动作元组，例如： (A,B)   (AB, C)
    :return: next_state: 下一个状态编码
    """
    (t1, t2) = action
    if len(t1) == 1 and len(t2) == 1:
        start_t1 = (ord(t1) - ord("A")) * 3
        start_t2 = (ord(t2) - ord("A")) * 3

        state[start_t1: start_t1 + 3] = [2, 3, 1]
        state[start_t2: start_t2 + 3] = [4, 5, 1]
        return state
    elif len(t1) != 1 and len(t2) == 1:
        start_t2 = (ord(t2) - ord("A")) * 3
        for table in t1:
            start = (ord(table) - ord("A")) * 3
            state[start: start + 3] = [num + 1 for num in state[start: start + 3]]
        rightest_start = (ord(t1[-1]) - ord("A")) * 3
        rightest_right = state[rightest_start + 1]
        rightest_layer = state[rightest_start + 2]
        t2_left = rightest_right + rightest_layer
        state[start_t2: start_t2 + 3] = [t2_left, t2_left + 1, state[start_t2 + 2] + 1]
        return state
    elif len(t1) != 1 and len(t2) != 1:
        # t1 全加一
        for table in t1:
            start = (ord(table) - ord("A")) * 3
            state[start: start + 3] = [num + 1 for num in state[start: start + 3]]
        # 获取最右表right及layer值         t2中所有编码 + right + 1
        rightest_start = (ord(t1[-1]) - ord("A")) * 3
        rightest_right = state[rightest_start + 1]
        rightest_layer = state[rightest_start + 2]
        for table in t2:
            start = (ord(table) - ord("A")) * 3
            state[start: start + 2] = [num + rightest_right + rightest_layer -1 for num in state[start: start + 2]]
            state[start + 2] = state[start + 2] + 1
        return state


if __name__ == '__main__':
    # a = TreeNode("x")
    # b = TreeNode("x")
    # c = TreeNode("D")
    # d = TreeNode("x")
    # e = TreeNode("C")
    # f = TreeNode("A")
    # g = TreeNode("B")
    # a.left = b
    # a.right = c
    # b.left = d
    # b.right = e
    # d.left = f
    # d.right = g
    # encoding(a)
    # print(code)

    # generate_exprs("stu teacher eply admin user")

    print(transition([2,3,1,4,5,1,2,3,1,4,5,1], ("AB", "CD")))

    # encode for 4 tables
    # with open("encoding_4t.txt","w") as f:
    #     codes = encode("((AB)(CD))")
    #     f.write("((AB)(CD)):\n" + str(codes) + "\n"*2)
    #     codes = encode("(((AB)C)D)")
    #     f.write("(((AB)C)D):\n" + str(codes) + "\n"*2)
    #     codes = encode("(((AB)D)C)")
    #     f.write("(((AB)D)C):\n" + str(codes) + "\n"*2)
    #
    #
    #     codes = encode("((AC)(BD))")
    #     f.write("((AC)(BD)):\n" + str(codes) + "\n"*2)
    #     codes = encode("(((AC)B)D)")
    #     f.write("(((AC)B)D):\n" + str(codes) + "\n"*2)
    #     codes = encode("(((AC)D)B)")
    #     f.write("(((AC)D)B):\n" + str(codes) + "\n"*2)
    #
    #
    #     codes = encode("((AD)(BC))")
    #     f.write("((AD)(BC)):\n" + str(codes) + "\n"*2)
    #     codes = encode("(((AD)B)C)")
    #     f.write("(((AD)B)C):\n" + str(codes) + "\n"*2)
    #     codes = encode("(((AD)C)B)")
    #     f.write("(((AD)C)B):\n" + str(codes) + "\n"*2)
    #
    #     codes = encode("(((BC)A)D)")
    #     f.write("(((BC)A)D):\n" + str(codes) + "\n"*2)
    #     codes = encode("(((BC)D)A)")
    #     f.write("(((BC)D)A):\n" + str(codes) + "\n"*2)
    #
    #
    #     codes = encode("(((BD)A)C)")
    #     f.write("(((BD)A)C):\n" + str(codes) + "\n"*2)
    #     codes = encode("(((BD)C)A)")
    #     f.write("(((BD)C)A):\n" + str(codes) + "\n"*2)
    #
    #
    #     codes = encode("(((CD)B)A)")
    #     f.write("(((CD)B)A):\n" + str(codes) + "\n"*2)
    #     codes = encode("(((CD)A)B)")
    #     f.write("(((CD)A)B):\n" + str(codes) + "\n"*2)

    # print("levelOrder:",end=' ')
    # levelOrder(a)
    # print("\nRecursionPreOrder:",end=' ')
    # RecursionPreOrder(a)
    # print("\nRecursionInOrder:",end=' ')
    # RecursionInOrder(a)
    # print("\nRecursionPostOrder:", end=' ')
    # RecursionPostOrder(a)
    # print("\nPreOrderWithoutRecursion:",end=' ')
    # PreOrderWithoutRecursion(a)
    # print("\nInOrderWithoutRecursion:",end=' ')
    # InOrderWithoutRecursion(a)
    # print("\nPostOrderWithoutRecursion:",end=' ')
    # PostOrderWithoutRecursion(a)
    # print("\nPostOrderWithoutRecursion_1:",end=' ')
    # PostOrderWithoutRecursion_1(a)
