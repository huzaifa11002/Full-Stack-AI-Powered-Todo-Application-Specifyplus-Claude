/**
 * Chat Page
 *
 * Protected route for AI chat interface with authentication check
 */

"use client";

import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import ChatInterface from "@/components/chat/ChatInterface";
import ChatErrorBoundary from "@/components/chat/ChatErrorBoundary";

export default function ChatPage() {
  const { user, isAuthenticated, isLoading: authLoading } = useAuth();
  const router = useRouter();

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      console.log("[ChatPage] Not authenticated, redirecting to login");
      router.push("/login");
    }
  }, [authLoading, isAuthenticated, router]);

  // Show loading state while checking auth
  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  // Don't render if not authenticated
  if (!isAuthenticated || !user) {
    return null;
  }

  return (
    <ChatErrorBoundary>
      <div className="min-h-screen bg-gray-50">
        <ChatInterface />
      </div>
    </ChatErrorBoundary>
  );
}
