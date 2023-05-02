from jamo import h2j, j2hcj
from g2pk import G2p
import re
def ipa_to_korean(ipa_string):
    """
    IPA 문자열을 한국어로 변환합니다.
    :param ipa_string: 변환할 IPA 문자열입니다.
    :return: 한국어로 변환된 문자열입니다.
    """
    ipa_to_korean = {
        "a": "ㅏ",
        "aː": "ㅏ",
        "b": "ㅂ",
        "e": "ㅔ",
        "eː": "ㅔ",
        "e̞": "ㅔ",
        "h": "ㅎ",
        "i": "ㅣ",
        "iː": "ㅣ",
        "j": "ㅈ",
        "k": "ㄱ",
        "kʰ": "ㅋ",
        "kˀ": "ㄲ",
        "l": "ㄹ",
        "lː": "ㄹ",
        "m": "ㅁ",
        "n": "ㄴ",
        "n̪": "ㄴ",
        "o": "ㅗ",
        "oː": "ㅗ",
        "p": "ㅍ",
        "pʰ": "ㅍ",
        "pˀ": "ㅃ",
        "s": "ㅅ",
        "sʰ": "ㅅ",
        "sˀ": "ㅆ",
        "s̪": "ㅅ",
        "s̪ˀ": "ㅆ",
        "t": "ㄷ",
        "tʰ": "ㅌ",
        "tˀ": "ㄸ",
        "t̠": "ㄷ",
        "t̪": "ㄷ",
        "t̪ʰ": "ㅌ",
        "t̪ˀ": "ㄸ",
        "u": "ㅜ",
        "uː": "ㅜ",
        "w": "ㅇ",
        "y": "ㅕ",
        "æ": "애",
        "æː": "애",
        "ø": "ㅚ",
        "ŋ": "ㅇ",
        "ɐ": "어",
        "ɕ": "시",
        "ɕʰ": "ㅊ",
        "ɘː": "어",
        "əː": "어",
        "ɛ": "에",
        "ɛː": "에",
        "ɛ̝": "에",
        "ɤ": "어",
        "ɤː": "어",
        "ɤ̞": "어",
        "ɨ": "이",
        "ɪ": "이",
        "ɯ": "우",
        "ɯː": "우",
        "ɾ": "ㄹ",
        "ʃ": "ㅅ",
        "ʃʰ": "ㅊ",
        "ʃˀ": "ㅆ",
        "ʌ": "어",
        "ʔ": "ㅇ",
        " ": " "
    }
    korean_string = ''
    ipa_words = ipa_string.split()
    for char in ipa_words:
        if char in ipa_to_korean:
            korean_string += ipa_to_korean[char]
        else:
            korean_string += char
    return korean_string

"""
def korean_to_ipa(korean_string):
    g2p = G2p()

    korean_dict = {
        'ㅏ': 'a',
        'ㅑ': 'ya',
        'ㅓ': 'ʌ',
        'ㅕ': 'yʌ',
        'ㅗ': 'o',
        'ㅛ': 'yo',
        'ㅜ': 'u',
        'ㅠ': 'yu',
        'ㅡ': 'ɯ',
        'ㅣ': 'i',
        'ㄱ': 'k̚',
        'ㄴ': 'n',
        'ㄷ': 't̚',
        'ㄹ': 'ɾ',
        'ㅁ': 'm',
        'ㅂ': 'p̚',
        'ㅅ': 's',
        'ㅇ': 'ŋ',
        'ㅈ': 'tɕ̚',
        'ㅊ': 'tɕʰ',
        'ㅋ': 'kʰ',
        'ㅌ': 'tʰ',
        'ㅍ': 'pʰ',
        'ㅎ': 'h',
        'ㅆ': 'ss',
        'ㅉ': 'jj',
        ' ' :' '
    }
    korean_input = text_to_phone(g2p(korean_string))
    ipa_string = ''
    for char in korean_input:
        for i in range(len(char)):
            if i == 0:
                print("초성", char[i])
                ipa_string += korean_dict[char[i]]
            elif i == len(char[i]) - 1:
                print("종성", char[i])
                ipa_string += korean_dict[char[i]]
            else:
                print("중성", char[i])
                ipa_string += korean_dict[char[i]]
    print(korean_string, " -->", g2p(korean_string), " --> ", ipa_string)
    return ipa_string
"""



def korean_to_ipa(hangul_string):
    # 한글 범위와 기본 자음, 모음 정의
    HANGUL_RANGE = re.compile("[가-힣]")
    BASE_CONSONANTS = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
    BASE_VOWELS = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"
    BASE_CONSONANTS_BOTTUM = "ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ"
    # 제한된 IPA 기호를 사용하여 자음과 모음 매핑
    LIMITED_IPA_CONSONANTS = {
        'ㄱ': 'k',
        'ㄲ': 'kʰ',
        'ㄴ': 'n',
        'ㄷ': 't',
        'ㄸ': 'tʰ',
        'ㄹ': 'l',
        'ㅁ': 'm',
        'ㅂ': 'p',
        'ㅃ': 'pʰ',
        'ㅅ': 's',
        'ㅆ': 'sʰ',
        'ㅇ': 'ŋ',
        'ㅈ': 'tʃ',
        'ㅉ': 'tʃʰ',
        'ㅊ': 'tʃʰ',
        'ㅋ': 'kʰ',
        'ㅌ': 'tʰ',
        'ㅍ': 'pʰ',
        'ㅎ': 'h'
    }
    LIMITED_IPA_VOWELS = {
        'ㅏ': 'a',
        'ㅐ': 'æ',
        'ㅑ': 'ja',
        'ㅒ': 'jæ',
        'ㅓ': 'ə',
        'ㅔ': 'e',
        'ㅕ': 'jə',
        'ㅖ': 'je',
        'ㅗ': 'o',
        'ㅘ': 'wa',
        'ㅙ': 'wæ',
        'ㅚ': 'ø',
        'ㅛ': 'jo',
        'ㅜ': 'u',
        'ㅝ': 'wə',
        'ㅞ': 'we',
        'ㅟ': 'y',
        'ㅠ': 'ju',
        'ㅡ': 'ɯ',
        'ㅢ': 'ɯi',
        'ㅣ': 'i'
    }

    ipa_string = ""
    g2p = G2p()
    for char in g2p(hangul_string):
        if HANGUL_RANGE.match(char):
            code = ord(char) - ord('가')
            initial = code // 588
            medial = (code % 588) // 28
            final = code % 28
            ipa_string += LIMITED_IPA_CONSONANTS[BASE_CONSONANTS[initial]]
            ipa_string += LIMITED_IPA_VOWELS[BASE_VOWELS[medial]]
            if final > 0:
                ipa_string += LIMITED_IPA_CONSONANTS[BASE_CONSONANTS_BOTTUM[final - 1]]
        elif char == " ":
            ipa_string += char
    #print(hangul_string, " -->", g2p(hangul_string), " --> ", ipa_string)
    return ipa_string









def text_to_phone(text):
    list = []
    for i in range(len(text)):
        list.append(j2hcj(h2j(text[i])))
    return list

def split_into_phonemes(korean_string):
    """
    한국어 문자열을 음소 단위로 분리합니다.
    :param korean_string: 분리할 한국어 문자열입니다.
    :return: 음소로 분리된 문자열입니다.
    """
    # 초성 리스트. 00 ~ 18
    CHOSUNG_LIST = [
        "ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ",
        "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ",
        "ㅆ", "ㅇ", "ㅈ", "ㅉ", "ㅊ",
        "ㅋ", "ㅌ", "ㅍ", "ㅎ"
    ]

    # 중성 리스트. 00 ~ 20
    JUNGSUNG_LIST = [
        "ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ",
        "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ",
        "ㅙ", "ㅚ", "ㅛ", "ㅜ", "ㅝ",
        "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ",
        "ㅣ"
    ]

    # 종성 리스트. 00 ~ 27 + 1(1개 없음)
    JONGSUNG_LIST = [
        "", "ㄱ", "ㄲ", "ㄳ", "ㄴ",
        "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ",
        "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㄿ",
        "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ",
        "ㅆ", "ㅇ", "ㅈ", "ㅊ", "ㅋ",
        "ㅌ", "ㅍ", "ㅎ"
    ]

    split_string = ""
    for char in korean_string:
        # 유니코드에서 한글은 0xAC00 으로부터
        # 초성 19개, 중성21개, 종성28개로 이루어지므로
        # 이들을 분리해낸다.
        char_code = ord(char) - 0xAC00
        if char_code > -1 and char_code < 11172:
            # 초성 = ((문자코드 - 0xAC00) / 28) / 21
            chosung_index = int(char_code / 28) // 21
            split_string += CHOSUNG_LIST[chosung_index]

            # 중성 = ((문자코드 - 0xAC00) / 28) % 21
            jungsung_index = int(char_code / 28) % 21
            split_string += JUNGSUNG_LIST[jungsung_index]

            # 종성 = (문자코드 - 0xAC00) % 28
            jongsung_index = char_code % 28
            if jongsung_index > 0:
                split_string += JONGSUNG_LIST[jongsung_index]
        else:
            split_string += char
    return split_string

if __name__ == '__main__':
    #test_code()
    #recorder = AudioRecorder()
    #recorder.streaming_start(model)
    #recorder.start()
    #recorder.record(0.18)  # 5초 동안 녹음
    #recorder.stop()
    #recorder.streaming_start(model)
    #recorder.gop_streaming_start(model, "가")

    #print(korean_to_ipa("나는 지금 테스트를 하고 있습니다"))

    #path = "C:/Users/sci/Desktop/KoreanDataset/train/wav/KsponSpeech_096789_1.wav"
    #print(path[:path.index("wav")] + "text/" + path[-len("KsponSpeech_000000_0.wav"):-4] + '.txt')
    #print(path[-12:-4])
    print(korean_to_ipa("날이 맑은 날에는 밖에 나가서 놀고 싶어요"))