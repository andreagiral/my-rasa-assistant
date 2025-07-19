from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import re
import boto3
from botocore.exceptions import ClientError
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os 
from openai import OpenAI
import logging
from typing import Any, Text, Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def fetch_html_from_s3(key: str) -> str:
    s3 = boto3.client("s3")
    bucket_name = "thinktrekai-openstax"
    logger.info(f"[S3 FETCH] Trying to fetch: {key}")
    try:
        obj = s3.get_object(Bucket=bucket_name, Key=key)
        content = obj['Body'].read().decode('utf-8')
        logger.info(f"[S3 FETCH SUCCESS] Successfully fetched: {key}")
        return content
    except ClientError as e:
        logger.warning(f"[S3 ERROR] Failed to retrieve {key}: {e}")
        return ""
    

def summarize_or_answer(prompt: str, context: str) -> str:
    try:
        logger.info(f"[OpenAI CALL] prompt: {prompt}")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful biology tutor who answers student questions using the OpenStax Biology 2e textbook."},
                {"role": "user", "content": f"{prompt}\n\nUse the following context:\n{context}"}
            ],
            max_tokens=400,
            temperature=0.7
        )
        content = response.choices[0].message.content
        if content:
            logger.info(f"[OpenAI RESPONSE] {content[:100]}...")
            return content.strip()
        else:
            logger.warning("[OpenAI WARNING] Empty content received.")
            return "Sorry, I couldn't generate a response at the moment."
    except Exception as e:
        logger.error(f"[OpenAI ERROR] {e}")
        return "Sorry, an error occurred while contacting OpenAI."

class ActionGetCapstoneIdea(Action):
    def name(self) -> Text:
        return "action_get_capstone_idea"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        user_message = tracker.latest_message.get("text", "").lower()
        match = re.search(r"capstone.*?(about|on|for)?\s*(.+)", user_message)
        topic = match.group(2) if match else "a biology topic"
        prompt = f"Suggest a creative, high school-level capstone project idea based on the topic: {topic}."
        context = "Topics should be grounded in biology and based on OpenStax Biology 2e where possible."
        response = summarize_or_answer(prompt, context)
        dispatcher.utter_message(response or "Sorry, I couldn't generate a capstone idea right now.")
        return []

class ActionGetBioContent(Action):
    def name(self) -> Text:
        return "action_get_bio_content"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        user_message = tracker.latest_message.get("text", "").lower()
        
       #if "capstone" in user_message:
           #logger.info("[ROUTE] Entered capstone project block")
           #match = re.search(r"capstone(?: (?:idea|project))?(?: about| on| for)?\s*(.+)", user_message)
           #if match:
            #   topic = match.group()
             #  prompt = f"Suggest a creative, high school-level or college capstone project idea based on the topic: {topic}."
              # context = "Topics should be grounded in biology and based on OpenStax Biology 2e where possible."
               #response = summarize_or_answer(prompt, context)
               #dispatcher.utter_message(response or "Sorry, I couldn't generate a capstone idea just now.")
           #else:
              #dispatcher.utter_message("What biology topic are you thinking of for your capstone project?")
              #return []

       #if not any(k in user_message for k in ["chapter", "section", "summary", "key terms", "review", "critical thinking", "visual"]):
        #   logger.info("[ROUTE] Entered general OpenAI Q&A block")
          # prompt = f"Answer this biology question clearly for a student: {user_message}"
          #response = summarize_or_answer(prompt, context="")
          #if response:
          #     dispatcher.utter_message(response)
           #else:
          #     dispatcher.utter_message("Sorry, I couldn’t understand your question.")
          # return []

        section_match = re.search(r"\b(\d{1,2})\.(\d)\b", user_message)
        chapter_match = re.search(r"chapter\s+(\d{1,2})", user_message)

        keywords = {
            "summary": "summary",
            "review": "review-questions",
            "key terms": "key-terms",
            "critical thinking": "critical-thinking",
            "visual": "visual-connection",
            "chapter": "chapter"
        }
        matched_keyword = next((k for k in keywords if k in user_message), None)

        s3_key = None
        if section_match:
            chapter_num, section_num = section_match.groups()
            unit = self.get_unit_for_chapter(int(chapter_num))
            s3_key = f"openstax_bio2e_chps/Unit {unit}/Chapter {int(chapter_num)}/{chapter_num}.{section_num}.html"
        elif chapter_match:
            chapter_num = int(chapter_match.group(1))
            unit = self.get_unit_for_chapter(chapter_num)
            if matched_keyword:
                file = keywords[matched_keyword]
                s3_key = f"openstax_bio2e_chps/Unit {unit}/Chapter {chapter_num}/{file}.html"
            else:
                s3_key = f"openstax_bio2e_chps/Unit {unit}/Chapter {chapter_num}/chapter-{chapter_num}.html"
        else:
            # General fallback question to OpenAI
            prompt = f"Answer this biology question clearly for a student: {user_message}"
            response = summarize_or_answer(prompt, context="")
            dispatcher.utter_message(response or "Sorry, I couldn’t answer that right now.")
            return []

        logger.info(f"[DEBUG] S3 key: {s3_key}")
        html = fetch_html_from_s3(s3_key)

        if not html:
            prompt = f"The student asked: '{user_message}'. Please answer as best you can based on general biology knowledge."
            fallback = summarize_or_answer(prompt, context="")
            dispatcher.utter_message(fallback)
            return []

        soup = BeautifulSoup(html, "html.parser")
        main = soup.find("main") or soup.body
        text = main.get_text("\n", strip=True) if main else soup.get_text("\n", strip=True)
        filtered = [line for line in text.splitlines() if not any(x in line.lower() for x in ["cookie", "consent", "privacy policy"])]
        cleaned = "\n".join(filtered)
        output = cleaned[:800] + "..." if len(cleaned) > 800 else cleaned
        dispatcher.utter_message(output)
        return []

    def get_unit_for_chapter(self, chapter: int) -> int:
        if 1 <= chapter <= 3: return 1
        if 4 <= chapter <= 10: return 2
        if 11 <= chapter <= 17: return 3
        if 18 <= chapter <= 20: return 4
        if 21 <= chapter <= 29: return 5
        if 30 <= chapter <= 32: return 6
        if 33 <= chapter <= 43: return 7
        if 44 <= chapter <= 47: return 8
        return 1
