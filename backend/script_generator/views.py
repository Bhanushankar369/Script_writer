from django.shortcuts import render

from .script_graph import graph_build

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Script
from .serializers import ScriptSerializer
from rapidfuzz import fuzz

# Create your views here.
class ScriptView(APIView):
    def post(self, request):
        message = f"""You are an expert YouTube Script Writer AI.

                    Your job is to generate highly engaging, well-structured, and audience-retentive video scripts based on:

                    You will ALWAYS receive the following inputs:

                    - title: {request.data.get('title')}
                    - context: {request.data.get('context')}
                    - video_length: {request.data.get('video_length')}
                    - category: {request.data.get('category')}
                    
                    They are already provided.
                    
                    STRICT RULES:
                    - Do NOT generate adult, sexual, or explicit content
                    - Do NOT generate illegal or harmful content
                    - Avoid sensitive or inappropriate topics
                    - If user asks such content, politely refuse

                    Instead respond:
                    "Sorry, I can't help with that request.

                    Follow these rules strictly:

                    1. Script Structure:
                    - Hook (first 5–10 seconds) – attention-grabbing opening
                    - Introduction
                    - Main Content (divided into logical sections)
                    - Call To Action (like, subscribe, comment)
                    - Outro

                    2. Length Control:
                    - Match the script to the requested video length.
                    - Approximate speaking speed: 130–160 words per minute.
                    - Adjust depth and detail accordingly.

                    3. Writing Style:
                    - Match tone to the category:
                        - Education → clear, structured, simple
                        - Tech → professional but friendly
                        - Entertainment → energetic and fun
                        - Motivation → emotional and inspiring
                        - Finance → confident and trustworthy
                    - Use short sentences.
                    - Speak directly to the viewer ("you").

                    4. Engagement Rules:
                    - Use storytelling where possible.
                    - Ask rhetorical questions.
                    - Use pattern interrupts every 30–45 seconds.
                    - Avoid monotone writing.

                    5. Output Format:

                    Return the script strictly in this format:

                    ---
                    TITLE: {request.data.get('title')}
                    
                    CONTEXT: {request.data.get('context')}

                    CATEGORY: {request.data.get('category')}

                    VIDEO LENGTH: {request.data.get('video_length')}

                    SCRIPT:

                    [HOOK]
                    ...

                    [INTRO]
                    ...

                    [MAIN CONTENT]
                    Section 1:
                    ...
                    Section 2:
                    ...
                    ...

                    [CALL TO ACTION]
                    ...

                    [OUTRO]
                    ...
                    ---

                    6. Do NOT include explanations or analysis.
                    7. Do NOT include markdown formatting.
                    8. Output only the final script.

                    If any input field is missing, ask for it before generating the script."""
                    
        def find_similar_context(newContext, oldContexts):
            best_score = 0
            best_match = None
            
            for script in oldContexts:
                score = fuzz.token_set_ratio(newContext.lower(), script.lower())
                
                if score > best_score:
                    best_score  = score
                    best_match = script
                    
            return best_score, best_match
                    
        scripts = Script.objects.all()
        oldContexts = {}
        
        for s in scripts:
            oldContexts[s.context] = s.ai_message
            
        newContext = request.data.get('context')
        
        score, match = find_similar_context(newContext, oldContexts.keys())
        
        
        banned_keywords = [
            # Adult / Sexual
            "porn", "porno", "pornography", "sex", "sexual", "nude", "naked", "xxx",
            "adult", "erotic", "intimate", "explicit", "nsfw", "fetish", "kinky",
            "bdsm", "seduce", "seduction", "arousal", "orgasm", "masturbate",
            "prostitute", "escort", "stripper", "lap dance", "onlyfans",

            # Illegal Activities
            "hack", "hacking", "bypass", "exploit", "crack", "piracy", "torrent",
            "dark web", "deep web", "illegal", "smuggling", "black market",
            "counterfeit", "forgery", "scam", "fraud", "identity theft",

            # Drugs / Substances
            "drugs", "cocaine", "heroin", "meth", "mdma", "lsd", "weed",
            "marijuana", "ganja", "opium", "drug trafficking", "overdose",

            # Violence / Harm
            "kill", "murder", "assassinate", "bomb", "explosive", "terrorist",
            "terrorism", "shoot", "gun attack", "massacre", "kidnap", "abuse",
            "self harm", "suicide", "hurt others",

            # Cybercrime / Security
            "phishing", "ddos", "malware", "ransomware", "spyware",
            "keylogger", "password crack", "brute force", "sql injection",
            "xss attack", "session hijack",

            # Sensitive / Inappropriate
            "hate speech", "racist", "extremist", "radicalize", "propaganda",
            "offensive content", "discrimination",

            # Misc Unsafe
            "illegal download", "cheat system", "bypass law", "fake identity",
            "impersonate", "steal data", "data leak", "leak database"
        ]
        
        for word in banned_keywords:
            if word in newContext:
                return Response({"Response": "This context contains sensitive and confidential information."})
        
        if score > 80:
            response = "This is from your own Database Cache. " + oldContexts[match]
        else:
            ai_response = graph_build.invoke({"messages": message})
            ai_ans = ai_response["messages"][-1]
            response = ai_ans.content

        data = request.data.copy()
        data['ai_message'] = response
        
        serializer = ScriptSerializer(data = data)
        
        if serializer.is_valid():
            serializer.save()
        
        return Response({"Response": serializer.data})