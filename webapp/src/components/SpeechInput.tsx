import React, { useState } from "react";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";
import { SpeechInputProps } from "../types";

const SpeechInput: React.FC<SpeechInputProps> = ({ onTranscript }) => {
  const [isListening, setIsListening] = useState(false);
  const { transcript, resetTranscript, browserSupportsSpeechRecognition } =
    useSpeechRecognition();

  if (!browserSupportsSpeechRecognition) {
    return <div>Browser doesn't support speech recognition.</div>;
  }

  const handleStart = () => {
    setIsListening(true);
    resetTranscript();
    SpeechRecognition.startListening({ continuous: true });
  };

  const handleStop = () => {
    setIsListening(false);
    SpeechRecognition.stopListening();
    if (transcript) {
      onTranscript(transcript);
    }
  };

  return (
    <div className="speech-input">
      <button
        onClick={isListening ? handleStop : handleStart}
        className={`speech-button ${isListening ? "listening" : ""}`}
      >
        {isListening ? "Stop Recording" : "Start Recording"}
      </button>
      {isListening && (
        <div className="transcript-preview">{transcript || "Speak now..."}</div>
      )}
    </div>
  );
};

export default SpeechInput;
