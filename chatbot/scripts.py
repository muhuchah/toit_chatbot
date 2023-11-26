from chatbot.services import read_jsonl_file, create_embedding
from chatbot.models import User, Chatbot, Chatbot_data
from pgvector.django import CosineDistance



def eval():
    user = User(username='test-user', password='test-user', can_make_chatbot=True)
    chatbot = Chatbot(name='test-chatbot', bio='test-chatbot', owner=user)
    user.save()
    chatbot.save()

    FILE_PATH = '/app/data.jsonl'
    jsonl_data = read_jsonl_file(FILE_PATH)

    for data in jsonl_data:
        chatbot_data = Chatbot_data(data=data['doc'][:800], embedding=create_embedding(data['doc']), chatbot=chatbot)
        chatbot_data.save()

    data_num = len(data)

    for data in jsonl_data:
        question_embed = create_embedding(data['question'])
        nearest_data = chatbot.chatbot_data_set.order_by(CosineDistance('embedding', question_embed))[:1]
        if nearest_data == data['doc']:
            similarity = similarity + 1

    print(similarity/data_num*100)