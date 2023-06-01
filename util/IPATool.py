from jamo import h2j, j2hcj
from g2pk import G2p
import re
def ipa_to_korean(ipa_string):
    """
    IPA 문자열을 한국어로 변환합니다.
    :param ipa_string: 변환할 IPA 문자열입니다.
    :return: 한국어로 변환된 문자열입니다.
    """
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
    LIMITED_KOREAN_CONSONANTS = {v: k for k, v in LIMITED_IPA_CONSONANTS.items()}
    LIMITED_KOREAN_VOWELS = {v: k for k, v in LIMITED_IPA_VOWELS.items()}
    korean_string = ''
    #ipa_list = split_ipa(ipa_string)
    for char in ipa_string:
        if char in LIMITED_KOREAN_CONSONANTS:
            korean_string += LIMITED_KOREAN_CONSONANTS[char]
        elif char in LIMITED_KOREAN_VOWELS:
            korean_string += LIMITED_KOREAN_VOWELS[char]
        else:
            korean_string += char
    return korean_string



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
    print(hangul_string, " -->", g2p(hangul_string), " --> ", ipa_string)
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

def get_highest_symbols(ipaInput):
    highest_symbols = []
    groups = ipaInput.split(" | ")
    for group in groups:
        values = group.split(" ")
        symbol_value_pairs = [(values[i], float(values[i + 1][1:-1])) for i in range(0, len(values), 2)]
        highest_symbol = max(symbol_value_pairs, key=lambda x: x[1])[0]
        highest_symbols.append(highest_symbol)
    return highest_symbols

def split_ipa(input_string):
    ipa_list = ['a', 'aː', 'b', 'e', 'eː', 'e̞', 'h', 'i', 'iː', 'j', 'k', 'kʰ', 'kˀ', 'l', 'lː', 'm', 'n', 'n̪', 'o',
                'oː', 'p', 'pʰ', 'pˀ', 's', 'sʰ', 'sˀ', 's̪', 's̪ˀ', 't', 'tʰ', 'tˀ', 't̠', 't̪', 't̪ʰ', 't̪ˀ', 'u',
                'uː', 'w', 'y', 'æ', 'æː', 'ø', 'ŋ', 'ɐ', 'ɕ', 'ɕʰ', 'ɘː', 'əː', 'ɛ', 'ɛː', 'ɛ̝', 'ɤ', 'ɤː', 'ɤ̞', 'ɨ',
                'ɪ', 'ɯ', 'ɯː', 'ɾ', 'ʃ', 'ʃʰ', 'ʃˀ', 'ʌ', 'ʔ']
    output = []
    index = 0
    while index < len(input_string):
        found = False
        for ipa in sorted(ipa_list, key=len, reverse=True):
            if input_string.startswith(ipa, index):
                output.append(ipa)
                index += len(ipa)
                found = True
                break
        if not found:
            index += 1
    return output


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
    print(ipa_to_korean(korean_to_ipa("마이크")))