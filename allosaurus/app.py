from allosaurus.am.utils import *
from pathlib import Path
from allosaurus.audio import read_audio, Audio
from allosaurus.pm.factory import read_pm
from allosaurus.am.factory import read_am
from allosaurus.lm.factory import read_lm
from allosaurus.bin.download_model import download_model
from allosaurus.model import resolve_model_name, get_all_models
from argparse import Namespace
from io import BytesIO

def read_recognizer(inference_config_or_name='latest', alt_model_path=None):
    if alt_model_path:
        if not alt_model_path.exists():
            download_model(inference_config_or_name, alt_model_path)
    # download specified model automatically if no model exists
    if len(get_all_models()) == 0:
        download_model('latest', alt_model_path)

    # create default config if input is the model's name
    if isinstance(inference_config_or_name, str):
        model_name = resolve_model_name(inference_config_or_name, alt_model_path)
        inference_config = Namespace(model=model_name, device_id=-1, lang='ipa', approximate=False, prior=None)
    else:
        assert isinstance(inference_config_or_name, Namespace)
        inference_config = inference_config_or_name

    if alt_model_path:
        model_path = alt_model_path / inference_config.model
    else:
        model_path = Path(__file__).parent / 'pretrained' / inference_config.model

    if inference_config.model == 'latest' and not model_path.exists():
        download_model(inference_config, alt_model_path)

    assert model_path.exists(), f"{inference_config.model} is not a valid model"

    # create pm (pm stands for preprocess model: audio -> feature etc..)
    pm = read_pm(model_path, inference_config)

    # create am (acoustic model: feature -> logits )
    am = read_am(model_path, inference_config)

    # create lm (language model: logits -> phone)
    lm = read_lm(model_path, inference_config)

    return Recognizer(pm, am, lm, inference_config)

class Recognizer:

    def __init__(self, pm, am, lm, config):

        self.pm = pm
        self.am = am
        self.lm = lm
        self.config = config

    def is_available(self, lang_id):
        # check whether this lang id is available

        return self.lm.inventory.is_available(lang_id)

    def recognize(self, filename, lang_id='kor', topk=1, emit=1.0, timestamp=False):
        # recognize a single file

        # filename check (skipping for BytesIO objects)
        if not isinstance(filename, BytesIO):
            assert str(filename).endswith('.wav'), "only wave file is supported in allosaurus"

        # load wav audio
        audio = read_audio(filename)
        # extract feature
        feat = self.pm.compute(audio)
        # add batch dim
        feats = np.expand_dims(feat, 0)
        feat_len = np.array([feat.shape[0]], dtype=np.int32)

        tensor_batch_feat, tensor_batch_feat_len = move_to_tensor([feats, feat_len], self.config.device_id)

        tensor_batch_lprobs = self.am(tensor_batch_feat, tensor_batch_feat_len)

        if self.config.device_id >= 0:
            batch_lprobs = tensor_batch_lprobs.cpu().detach().numpy()
        else:
            batch_lprobs = tensor_batch_lprobs.detach().numpy()

        token = self.lm.compute(batch_lprobs[0], lang_id, topk, emit=emit, timestamp=timestamp)
        return token

    def streaming_setting(self, channel_number, framerate, nframesm, sampwidth):
        self.channel_number = channel_number
        self.framerate = framerate
        self.nframes = nframesm
        self.sampwidth = sampwidth
        print("Streaming Setting Complete")

    def recognize_Streaming(self, data, lang_id='kor', topk=1, emit=1.0, timestamp=False, channel=0, header_only=False):
        # recognize a single file
        audio = Audio()
        # set stream basic info
        channel_number = self.channel_number
        # print("Check_wf_nChannels", self.channel_number)
        # check the input channel is valid
        assert channel < channel_number
        # print("Check_wf_framerate", self.framerate)
        # print("Check_wf_nframes", self.nframes)
        # print("Check_wf_sampwidth", self.sampwidth)
        # set wav header
        audio.set_header(sample_rate=self.framerate, sample_size=len(data), channel_number=1,
                         sample_width=self.sampwidth)
        # set audio
        if not header_only:
            # print("Check_wf_x", len(data))
            assert (channel_number <= 2)

            audio_bytes = np.frombuffer(data, dtype='int16')

            # get the first channel if stereo
            if channel_number == 2:
                audio_bytes = audio_bytes[channel::2]

            audio.samples = audio_bytes

            # when some utils piping to stdout, sample size might not be correct (e.g: lame --decode)
            audio.sample_size = len(audio.samples)

        # extract feature
        feat = self.pm.compute(audio)
        # add batch dim
        feats = np.expand_dims(feat, 0)
        feat_len = np.array([feat.shape[0]], dtype=np.int32)

        tensor_batch_feat, tensor_batch_feat_len = move_to_tensor([feats, feat_len], self.config.device_id)

        tensor_batch_lprobs = self.am(tensor_batch_feat, tensor_batch_feat_len)

        if self.config.device_id >= 0:
            batch_lprobs = tensor_batch_lprobs.cpu().detach().numpy()
        else:
            batch_lprobs = tensor_batch_lprobs.detach().numpy()

        token = self.lm.compute(batch_lprobs[0], lang_id, topk, emit=emit, timestamp=timestamp)
        return token