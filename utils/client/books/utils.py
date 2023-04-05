import os


def file_into_bytecode(file_path):
    with open(file_path, 'rb') as file:
        bytecode_file = file.read()
    return bytecode_file


def file_from_bytecode(filename, byte_data):
    with open(filename, 'wb') as file:
        file.write(byte_data)


def get_data_dict(directory, data, with_id: bool = None):
    id_num: int = 1
    for dir in os.listdir(directory):
        data[dir] = {}
        book = data[dir]
        authors_dir = os.path.join(directory, dir)
        book["authors"] = []
        for author in os.listdir(authors_dir):
            author_detail_root = os.path.join(authors_dir, author)
            book['authors'].append(
                {
                    author: {
                        "name": author, "cover": os.path.join(author_detail_root, "cover.jpg").replace('\\', "/"),
                        "pdf": os.path.join(author_detail_root, "pdf.pdf").replace('\\', '/')}
                }
            )
            if with_id:
                book['authors'][-1][author]["id"] = id_num
                id_num += 1
    return data


def get_data_in_tuples(data):
    _list = []
    for lesson in data:
        for book in data[lesson]['authors']:
            for k, v in book.items():
                _list.append(tuple(v.values()))
    return _list
