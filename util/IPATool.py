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
    i = 0
    while i < len(ipa_string):
        # 두 글자 조합 시도
        if i + 1 < len(ipa_string):
            two_char_combination = ipa_string[i:i+2]
            if two_char_combination in LIMITED_KOREAN_CONSONANTS:
                korean_string += LIMITED_KOREAN_CONSONANTS[two_char_combination]
                i += 2
                continue
            elif two_char_combination in LIMITED_KOREAN_VOWELS:
                korean_string += LIMITED_KOREAN_VOWELS[two_char_combination]
                i += 2
                continue

        # 두 글자 조합이 없으면 한 글자만 변환
        if ipa_string[i] in LIMITED_KOREAN_CONSONANTS:
            korean_string += LIMITED_KOREAN_CONSONANTS[ipa_string[i]]
        elif ipa_string[i] in LIMITED_KOREAN_VOWELS:
            korean_string += LIMITED_KOREAN_VOWELS[ipa_string[i]]
        #else:
        #    korean_string += ipa_string[i]

        i += 1

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
    return [ipa_string, g2p(hangul_string), ipa_string]


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
    highest_symbols = ""
    groups = ipaInput.split(" | ")
    for group in groups:
        values = group.split(" ")
        symbol_value_pairs = [(values[i], float(values[i + 1][1:-1])) for i in range(0, len(values), 2)]
        highest_symbol = max(symbol_value_pairs, key=lambda x: x[1])[0]
        highest_symbols += highest_symbol
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

def hangul_letter_combiner(choseong, jungseong, jongseong=None):
    """
    초성, 중성, 종성을 받아 한글 글자를 조합하는 함수입니다.
    :param choseong: 한글 초성 (예: 'ㄱ', 'ㄴ')
    :param jungseong: 한글 중성 (예: 'ㅏ', 'ㅣ')
    :param jongseong: 한글 종성, 없는 경우 None (예: 'ㄱ', None)
    :return: 조합된 한글 글자 (예: '가', '안')
    """
    # 한글 유니코드 시작점 및 초성, 중성, 종성의 기본 위치
    HANGUL_START = 0xAC00
    CHO_BASE = 588
    JUNG_BASE = 28

    # 한글 초성, 중성, 종성 리스트
    choseongs = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    jungseongs = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
    jongseongs = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

    # 초성, 중성, 종성의 유니코드 인덱스 계산
    unicode_index = HANGUL_START + (choseongs.index(choseong) * CHO_BASE) + (jungseongs.index(jungseong) * JUNG_BASE)

    # 종성이 있는 경우 인덱스 추가
    if jongseong is not None:
        unicode_index += jongseongs.index(jongseong)

    # 계산된 유니코드 인덱스로부터 한글 글자 생성
    return chr(unicode_index)



def string_to_hangul(input_string):
    # 한글 초성, 중성, 종성 리스트
    choseongs = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    jungseongs = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
    jongseongs = ['', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

    result = ""
    i = 0
    while i < len(input_string):
        choseong = jungseong = jongseong = None

        # 초성 확인
        if i < len(input_string) and input_string[i] in choseongs:
            choseong = input_string[i]
            i += 1
        else:
            choseong = 'ㅇ'  # 초성이 없는 경우 'ㅇ'으로 처리

        # 중성 확인
        if i < len(input_string) and input_string[i] in jungseongs:
            jungseong = input_string[i]
            i += 1

        # 종성 확인 (다음 글자가 초성인 경우에만 종성으로 처리)
        if i < len(input_string) and input_string[i] in jongseongs and (i + 1 == len(input_string) or input_string[i + 1] in choseongs):
            jongseong = input_string[i]
            i += 1

        # 한글 글자 조합
        if choseong and jungseong:
            combined_letter = hangul_letter_combiner(choseong, jungseong, jongseong)
            result += combined_letter

    return result


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
    stringchecker = ipa_to_korean(korean_to_ipa("스마트폰"))

    print("Result 1: ",stringchecker)
    print("Result 2: ",string_to_hangul(stringchecker))