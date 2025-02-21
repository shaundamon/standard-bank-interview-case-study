import { useCallback, useEffect, useState } from 'react';
import { useSettingsStore } from '../store/settingsStore';

export const useSpeechSynthesis = () => {
  const [voices, setVoices] = useState<SpeechSynthesisVoice[]>([]);
  const [speaking, setSpeaking] = useState(false);
  const { isScreenReaderEnabled } = useSettingsStore();

  useEffect(() => {
    const loadVoices = () => {
      setVoices(window.speechSynthesis.getVoices());
    };

    window.speechSynthesis.addEventListener('voiceschanged', loadVoices);
    loadVoices();

    return () => {
      window.speechSynthesis.removeEventListener('voiceschanged', loadVoices);
    };
  }, []);

  const speak = useCallback(
    (text: string) => {
      if (!isScreenReaderEnabled) return;

      // Cancel any ongoing speech
      window.speechSynthesis.cancel();

      const utterance = new SpeechSynthesisUtterance(text);

      // Find an English voice
      const englishVoice = voices.find((voice) => voice.lang.startsWith('en-'));
      if (englishVoice) {
        utterance.voice = englishVoice;
      }

      // event handlers
      utterance.onstart = () => setSpeaking(true);
      utterance.onend = () => setSpeaking(false);
      utterance.onerror = () => setSpeaking(false);

      window.speechSynthesis.speak(utterance);
    },
    [voices, isScreenReaderEnabled]
  );

  const cancel = useCallback(() => {
    window.speechSynthesis.cancel();
    setSpeaking(false);
  }, []);

  return { speak, cancel, speaking };
};