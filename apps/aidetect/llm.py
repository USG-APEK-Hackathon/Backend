import os
import langchain
from langchain_openai import OpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.question_answering import load_qa_chain
from decouple import config

pdf_path = "/home/kazimovzaman2/Backend-Hackathon/apps/aidetect/llm.pdf"
openai_api_key = config("OPENAI_API_KEY")

loader = PyPDFLoader(pdf_path)
documents = loader.load()

llm = OpenAI(openai_api_key=openai_api_key)

chain = load_qa_chain(llm, verbose=True)


def process_message(message):

    template = """
     Verilən sualı ingiliscəyə tərcümə et cavabı hazırla, sonradan cavabı azərbaycanca tərcümə et.
    """

    response = "PAŞA Həyat Sığorta şirkəti, müxtəlif həyat sığortası məhsulları təklif edir, o cümlədən \"Həyatın Yaşam Sığortası\" ki, əməkhaqqınızın bir hissəsini sığortaya yönləndirərək vergi və sosial sığorta ödənişlərinizin qaytarılmasını və əlavə əmanət faizini təmin edir. Qoşulma prosesi çevikdir, minimal 50 AZN ilə başlayır və avtomatik ödənişlər vasitəsilə həyata keçirilir. Daha ətraflı məlumat və qoşulmaq üçün PAŞA Həyatın rəsmi veb saytını ziyarət edə bilərsiniz."
    return response
