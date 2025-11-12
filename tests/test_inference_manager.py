from facefusion import content_analyser


def test_collect_model_downloads_is_empty() -> None:
	model_hash_set, model_source_set = content_analyser.collect_model_downloads()
	assert model_hash_set == {}
	assert model_source_set == {}


def test_analyse_helpers_always_return_false() -> None:
	assert content_analyser.analyse_frame(None) is False  # type: ignore[arg-type]
	assert content_analyser.analyse_stream(None, 30.0) is False  # type: ignore[arg-type]
	assert content_analyser.analyse_image('dummy') is False
	assert content_analyser.analyse_video('dummy', 0, 1) is False
