from email.generator import Generator
import enum
from re import A
import pyttsx3 as tts
from pyttsx3.voice import Voice as ttsVoice
import googletrans
from googletrans.models import Translated as gtTranslated
from typing import List
import random


class SpeechTranslator:
    class VoiceGender(enum.Enum):
        MALE = "VoiceGenderMale"
        FEMALE = "VoiceGenderFemale"

    def __init__(
        self, default_voice_id: str = "com.apple.speech.synthesis.voice.samantha"
    ):
        self.translate_engine = googletrans.Translator()
        self.tts_engine = tts.init()
        self.default_voice_id = default_voice_id

    def translate_text(self, text: str, dest: str, src: str = "auto") -> gtTranslated:
        translated = self.translate_engine.translate(text, dest=dest, src=src)
        return translated

    def read_text(self, text: str, voice: ttsVoice) -> None:
        self.tts_engine.setProperty("voice", voice.id)
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def get_voice(
        self,
        name: str = None,
        language: str = None,
        gender: VoiceGender = None,
        *args,
        **kwargs
    ) -> ttsVoice:
        voices = self.tts_engine.getProperty("voices")

        def conditions(voice: ttsVoice) -> bool:
            language_codes = [lang[:2] for lang in voice.languages]
            by_language = language in language_codes if language else True
            by_gender = voice.gender == gender.value if gender else True
            by_name = voice.name == name if name else True
            return by_language and by_gender and by_name

        return random.choice(
            list(filter(conditions, voices))
            or list(filter(lambda v: v.id == self.default_voice_id, voices))
        )

    def read_translated(
        self, text: str, to_lang: str, from_lang: str = None, *args, **kwargs
    ) -> None:
        translated = (
            self.translate_text(text, to_lang, from_lang)
            if from_lang
            else self.translate_text(text, to_lang)
        )
        voice = self.get_voice(**{"language": translated.dest, **kwargs})
        self.read_text(translated.text, voice)

if __name__ == "__main__":
    SpeechTranslator().read_translated(
        "Informar a la administradora de riesgos laborales la modalidad de trabajo elegido",
        "es",
        gender=SpeechTranslator.VoiceGender.FEMALE,
    )
