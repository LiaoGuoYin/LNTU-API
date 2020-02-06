from aipao.core import Client


def run(request):
    print("Starting")
    for id in range(209000, 808589):
        try:
            client = Client(id)
            if client.student.total_records == 0:
                continue
            pages = (client.student.success_records // 20) + 1
            for page in range(pages):
                client.getSuccess(pageNo=page)
            pages = (client.student.failure_records // 20) + 1
            for page in range(pages):
                client.getFailure(pageNo=page)
        except Exception as e:
            print(e)
