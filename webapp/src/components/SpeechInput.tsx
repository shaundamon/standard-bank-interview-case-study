import { useState, useCallback } from "react";
import SpeechRecognition, {
  useSpeechRecognition as useBrowserSpeechRecognition,
} from "react-speech-recognition";
import { useSpeechSynthesis } from "../hooks/useSpeechSynthesis";

export const useSpeechRecognition = () => {
  const [isRecording, setIsRecording] = useState(false);
  const { speak } = useSpeechSynthesis();

  const { transcript, resetTranscript, browserSupportsSpeechRecognition } =
    useBrowserSpeechRecognition();

  const startRecording = useCallback(() => {
    if (!browserSupportsSpeechRecognition) {
      speak("Your browser doesn't support speech recognition");
      return;
    }
    setIsRecording(true);
    resetTranscript();
    SpeechRecognition.startListening({ continuous: true });
    speak("Recording started");
  }, [speak, browserSupportsSpeechRecognition, resetTranscript]);

  const stopRecording = useCallback(() => {
    if (isRecording) {
      SpeechRecognition.stopListening();
      setIsRecording(false);
      speak("Recording stopped");
    }
  }, [isRecording, speak]);

  return {
    isRecording,
    transcript,
    startRecording,
    stopRecording,
    browserSupportsSpeechRecognition,
  };
};
