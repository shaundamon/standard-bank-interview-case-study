import { useCallback, useEffect, useState } from 'react';
import { useSettingsStore } from '../store/settingsStore';

export const useSpeechSynthesis = () => {
  const [voices, setVoices] = useState<SpeechSynthesisVoice[]>([]);
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

      const utterance = new SpeechSynthesisUtterance(text);
      const englishVoice = voices.find((voice) => voice.lang.startsWith('en-'));
      if (englishVoice) {
        utterance.voice = englishVoice;
      }
      window.speechSynthesis.speak(utterance);
    },
    [voices, isScreenReaderEnabled]
  );

  return { speak };
};