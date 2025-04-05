
import { useRef, useEffect, useState } from "react";
import { useSpeechSynthesis } from 'react-speech-kit';
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Bot, User, BookOpen, Stethoscope, HeartHandshake, UserRound } from "lucide-react";
import { Message } from "@/types/message";

interface MessageAreaProps {
  messages: Message[];
}

const AgentIcon = ({ agentName }: { agentName?: string }) => {
  switch (agentName?.toLowerCase()) {
    case "flock":
      return <BookOpen className="h-6 w-6 text-blue-600 dark:text-blue-300" />;
    case "mia":
      return <HeartHandshake className="h-6 w-6 text-amber-600 dark:text-amber-300" />;
    case "doctor strange":
    case "doctor_strange":
      return <Stethoscope className="h-6 w-6 text-green-600 dark:text-green-300" />;
    case "sara":
      return <UserRound className="h-6 w-6 text-red-600 dark:text-red-300" />;
    default:
      return <Bot className="h-6 w-6 text-purple-600 dark:text-purple-300" />;
  }
};

const getAvatarBackground = (agentName?: string) => {
  switch (agentName?.toLowerCase()) {
    case "flock":
      return "bg-blue-100 dark:bg-blue-900/30";
    case "mia":
      return "bg-amber-100 dark:bg-amber-900/30";
    case "doctor strange":
    case "doctor_strange":
      return "bg-green-100 dark:bg-green-900/30";
    case "sara":
      return "bg-red-100 dark:bg-red-900/30";
    default:
      return "bg-purple-100 dark:bg-purple-900/30";
  }
};

const MessageArea = ({ messages }: MessageAreaProps) => {
  const messageEndRef = useRef<HTMLDivElement>(null);
  const { speak, cancel, speaking } = useSpeechSynthesis();
  const [spokenMessageIds, setSpokenMessageIds] = useState<Set<number>>(new Set());

  // Auto-scroll to the latest message and read new AI messages
  useEffect(() => {
    if (messageEndRef.current) {
      messageEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
    
    // Read only the latest AI message if it hasn't been spoken yet
    if (messages.length > 0) {
      const lastMessageIndex = messages.length - 1;
      const lastMessage = messages[lastMessageIndex];
      
      if (!lastMessage.isUser && !spokenMessageIds.has(lastMessageIndex)) {
        // Cancel any ongoing speech before starting new one
        if (speaking) {
          cancel();
        }
        speak({ text: lastMessage.text });
        
        // Mark this message as spoken
        setSpokenMessageIds(prev => {
          const newSet = new Set(prev);
          newSet.add(lastMessageIndex);
          return newSet;
        });
      }
    }
  }, [messages, speak, cancel, speaking, spokenMessageIds]);

  // Show all messages instead of just the latest one
  return (
    <ScrollArea className="flex-grow">
      <div className="flex-grow p-4 overflow-y-auto bg-white dark:bg-gray-900 min-h-full">
        {messages.length === 0 ? (
          <div className="h-full flex items-center justify-center">
            <div className="text-center max-w-md p-6 rounded-lg bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm shadow-sm">
              <p className="text-gray-500 dark:text-gray-400">
                Type something below to start the conversation.
              </p>
            </div>
          </div>
        ) : (
          <div className="space-y-4 animate-fade-in">
            {messages.map((message, index) => (
              <div key={index} className="flex items-start gap-3">
                {message.isUser ? (
                  <>
                    <div className="flex-1"></div>
                    <div className="py-3 px-4 rounded-lg shadow-sm bg-blue-50 dark:bg-blue-900/30 text-gray-800 dark:text-gray-200 border border-blue-100 dark:border-blue-900/30 rounded-tr-none">
                      {message.text}
                    </div>
                    <Avatar className="h-12 w-12 mt-1">
                      <AvatarFallback className="bg-blue-100 dark:bg-blue-900/30">
                        <User className="h-6 w-6 text-blue-600 dark:text-blue-300" />
                      </AvatarFallback>
                    </Avatar>
                  </>
                ) : (
                  <>
                    <Avatar className="h-12 w-12 mt-1">
                      <AvatarFallback className={getAvatarBackground(message.agent_name)}>
                        <AgentIcon agentName={message.agent_name} />
                      </AvatarFallback>
                    </Avatar>
                    <div className="py-3 px-4 rounded-lg shadow-sm bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200 border border-purple-100 dark:border-purple-900/30 rounded-tl-none flex-1">
                      {message.text}
                    </div>
                  </>
                )}
              </div>
            ))}
            <div ref={messageEndRef} />
          </div>
        )}
      </div>
    </ScrollArea>
  );
};

export default MessageArea;
