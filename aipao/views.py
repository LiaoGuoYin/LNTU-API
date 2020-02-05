from spider.core import Client


def run(request):
    print("Starting")
    for id in range(500000, 900000):
        try:
            client = Client(id)
            print(client)
            pages = client.student.success_records // 20
            for page in range(pages):
                client.getSuccess(pageNo=page)
            pages = client.student.failure_records // 20
            for page in range(pages):
                client.getFailure(pageNo=page)
        except Exception as e:
            print(e)
