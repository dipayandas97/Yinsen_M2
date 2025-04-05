
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { ArrowRight, Loader2, Sparkles, Mic, X } from "lucide-react";
import { useEffect, useState, useCallback } from "react";

interface MessageInputProps {
  currentMessage: string;
  setCurrentMessage: (message: string) => void;
  handleSendMessage: (message: string) => void;
  isLoading: boolean;
}

const MessageInput = ({ 
  currentMessage, 
  setCurrentMessage, 
  handleSendMessage,
  isLoading
}: MessageInputProps) => {
  const [isRecording, setIsRecording] = useState(false);
  const [isPushToTalkActive, setIsPushToTalkActive] = useState(false);
  const [recognition, setRecognition] = useState<SpeechRecognition | null>(null);
  const [transcript, setTranscript] = useState("");
  
  // Set up speech recognition
  useEffect(() => {
    if (typeof window !== 'undefined') {
      // Browser compatibility check
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      
      if (SpeechRecognition) {
        const recognitionInstance = new SpeechRecognition();
        recognitionInstance.continuous = true;
        recognitionInstance.interimResults = true;
        recognitionInstance.lang = 'en-US';
        
        recognitionInstance.onresult = (event) => {
          const current = event.resultIndex;
          const currentTranscript = event.results[current][0].transcript;
          
          // Update local transcript state
          setTranscript(prev => {
            const newTranscript = prev ? prev + ' ' + currentTranscript : currentTranscript;
            return newTranscript.trim();
          });
          
          // Update the current message with the full transcript
          setCurrentMessage((transcript + ' ' + currentTranscript).trim());
        };
        
        recognitionInstance.onerror = (event) => {
          console.error('Speech recognition error', event.error);
          stopRecording();
        };
        
        setRecognition(recognitionInstance);
      }
    }
    
    return () => {
      if (recognition) {
        recognition.stop();
      }
    };
  }, []);
  
  // Update currentMessage whenever transcript changes
  useEffect(() => {
    if (transcript) {
      setCurrentMessage(transcript);
    }
  }, [transcript, setCurrentMessage]);
  
  const startRecording = useCallback(() => {
    if (recognition) {
      setIsRecording(true);
      setTranscript("");
      setCurrentMessage("");
      recognition.start();
    }
  }, [recognition, setCurrentMessage]);
  
  const stopRecording = useCallback(() => {
    if (recognition) {
      setIsRecording(false);
      recognition.stop();
    }
  }, [recognition]);
  
  const handleStartPushToTalk = useCallback(() => {
    setIsPushToTalkActive(true);
    startRecording();
  }, [startRecording]);
  
  const handleEndPushToTalk = useCallback(() => {
    setIsPushToTalkActive(false);
    stopRecording();
  }, [stopRecording]);
  
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage(currentMessage);
    }
  };

  return (
    <div className="p-5 border-t border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 sticky bottom-0 backdrop-blur-sm">
      <div className="flex flex-col gap-2 max-w-4xl mx-auto">
        {isLoading && (
          <div className="text-xs text-center text-blue-500 dark:text-blue-400 animate-pulse">
            {/* Show more detailed status message when loading */}
            Connecting to AI backend... If this takes too long, the server might be unavailable or have CORS issues.
          </div>
        )}
        {isRecording && (
          <div className="text-xs text-center text-red-500 dark:text-red-400 animate-pulse flex items-center justify-center gap-2">
            <span className="h-2 w-2 bg-red-500 dark:bg-red-400 rounded-full"></span>
            Recording... Speak now
          </div>
        )}
        <div className="flex items-center gap-3">
          <Sparkles className="h-5 w-5 text-blue-500 dark:text-blue-400 animate-pulse" />
          <Input
            value={currentMessage}
            onChange={(e) => setCurrentMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={isRecording ? "Listening..." : "Type something..."}
            className="flex-grow border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800 focus-visible:ring-blue-500"
            disabled={isLoading || isRecording}
          />
          
          {/* Toggle record button */}
          {!isRecording ? (
            <Button
              type="button"
              size="icon"
              variant="outline"
              className="rounded-full bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700"
              onClick={startRecording}
              disabled={isLoading || !recognition}
              title="Start recording"
            >
              <Mic className="h-4 w-4 text-gray-600 dark:text-gray-400" />
            </Button>
          ) : (
            <Button
              type="button"
              size="icon"
              variant="outline"
              className="rounded-full bg-red-100 hover:bg-red-200 dark:bg-red-900 dark:hover:bg-red-800"
              onClick={stopRecording}
              title="Stop recording"
            >
              <X className="h-4 w-4 text-red-600 dark:text-red-400" />
            </Button>
          )}
          
          {/* Push-to-talk button */}
          <Button
            type="button"
            size="icon"
            variant="outline"
            className={`rounded-full ${
              isPushToTalkActive 
                ? "bg-red-100 hover:bg-red-200 dark:bg-red-900 dark:hover:bg-red-800" 
                : "bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700"
            }`}
            onMouseDown={handleStartPushToTalk}
            onMouseUp={handleEndPushToTalk}
            onMouseLeave={isPushToTalkActive ? handleEndPushToTalk : undefined}
            onTouchStart={handleStartPushToTalk}
            onTouchEnd={handleEndPushToTalk}
            disabled={isLoading || !recognition}
            title="Push to talk"
          >
            <Mic className={`h-4 w-4 ${
              isPushToTalkActive 
                ? "text-red-600 dark:text-red-400" 
                : "text-gray-600 dark:text-gray-400"
            }`} />
          </Button>
          
          {/* Send button */}
          <Button 
            onClick={() => handleSendMessage(currentMessage)}
            disabled={!currentMessage.trim() || isLoading}
            size="icon"
            className="bg-blue-600 hover:bg-blue-700 shadow-md hover:shadow-lg transition-all"
          >
            {isLoading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <ArrowRight className="h-4 w-4" />
            )}
          </Button>
        </div>
      </div>
    </div>
  );
};

export default MessageInput;
