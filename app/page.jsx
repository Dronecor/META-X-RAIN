'use client';

import { useState, useEffect, useRef } from 'react';
import ChatMessage from './components/ChatMessage';
import LoginForm from './components/LoginForm';
import OrderDetails from './components/OrderDetails';
import styles from './page.module.css';

const API_URL = process.env.NEXT_PUBLIC_BACKEND_API_URL || 'http://localhost:8000/api/v1';

// Helper function to generate contextual title from first 2 user messages using AI
const generateSmartTitle = async (messages) => {
    try {
        // Get first 2 user messages
        const userMessages = messages.filter(m => m.role === 'user').slice(0, 2);
        if (userMessages.length === 0) return 'New Chat';

        const combinedText = userMessages.map(m => m.content).join('. ');

        // Simple client-side summarization (first 5 words)
        const words = combinedText.split(' ').slice(0, 5).join(' ');
        return words.length > 35 ? words.substring(0, 35) + '...' : words;
    } catch (error) {
        console.error('Error generating title:', error);
        return 'New Chat';
    }
};

// Helper function to format timestamp
const formatTimestamp = (date) => {
    const now = new Date();
    const diff = now - date;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 1) return 'Just now';
    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    if (days < 7) return `${days}d ago`;
    return date.toLocaleDateString();
};

export default function Home() {
    const [user, setUser] = useState(null);
    const [conversations, setConversations] = useState({});
    const [activeConversationId, setActiveConversationId] = useState(null);
    const [inputValue, setInputValue] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const [orders, setOrders] = useState([]);
    const [selectedOrder, setSelectedOrder] = useState(null);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const currentMessages = activeConversationId ? conversations[activeConversationId]?.messages || [] : [];

    useEffect(() => {
        scrollToBottom();
    }, [currentMessages]);

    // Fetch user's orders when logged in
    useEffect(() => {
        if (user) {
            fetchOrders();
        }
    }, [user]);

    const fetchOrders = async () => {
        try {
            // Mock orders with more details - replace with actual API call
            setOrders([
                {
                    id: 1001,
                    item: 'Blue Summer Dress',
                    status: 'Shipped',
                    date: '2025-12-05',
                    price: 89.99,
                    quantity: 1,
                    trackingNumber: 'TRK123456789',
                    estimatedDelivery: '2025-12-10'
                },
                {
                    id: 1002,
                    item: 'Black Leather Jacket',
                    status: 'Processing',
                    date: '2025-12-07',
                    price: 199.99,
                    quantity: 1
                },
                {
                    id: 1003,
                    item: 'White Sneakers',
                    status: 'Pending',
                    date: '2025-12-08',
                    price: 79.99,
                    quantity: 2
                },
            ]);
        } catch (error) {
            console.error('Error fetching orders:', error);
        }
    };

    const handleCancelOrder = async (orderId) => {
        try {
            // TODO: Call backend API to cancel order
            // await fetch(`${API_URL}/orders/${orderId}/cancel`, { method: 'POST' });

            // Update local state
            setOrders(orders.map(order =>
                order.id === orderId ? { ...order, status: 'Cancelled' } : order
            ));
            setSelectedOrder(null);
            alert('Order cancelled successfully');
        } catch (error) {
            console.error('Error cancelling order:', error);
            alert('Failed to cancel order. Please try again.');
        }
    };



    const handleImageUpload = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        // Add optimistic user message with image
        const localImageUrl = URL.createObjectURL(file);
        const updatedMessages = [...currentMessages, {
            role: 'user',
            content: `[Image Uploaded] Finding similar items...`,
            image_url: localImageUrl
        }];

        setConversations({
            ...conversations,
            [activeConversationId]: {
                ...conversations[activeConversationId],
                messages: updatedMessages,
            },
        });

        setIsLoading(true);

        try {
            // Upload to backend
            const formData = new FormData();
            formData.append('file', file);

            const uploadRes = await fetch(`${API_URL}/utils/upload`, {
                method: 'POST',
                body: formData
            });

            if (!uploadRes.ok) throw new Error('Upload failed');

            const { url } = await uploadRes.json();
            // Append backend base URL if relative
            const fullImageUrl = url.startsWith('http') ? url : `${API_URL.replace('/api/v1', '')}${url}`;

            // Send to chat with image_url
            const userMessage = "Find products like this";

            const response = await fetch(`${API_URL}/chat/message`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: userMessage,
                    image_url: fullImageUrl,
                    user_id: user.email,
                    user_name: user.full_name,
                    email: user.email,
                }),
            });

            if (response.ok) {
                const data = await response.json();
                const finalMessages = [...updatedMessages, { role: 'assistant', content: data.response }];

                setConversations((prev) => ({
                    ...prev,
                    [activeConversationId]: {
                        ...prev[activeConversationId],
                        messages: finalMessages,
                    },
                }));
            }
        } catch (error) {
            console.error('Visual Search Error:', error);
            // Handle error in UI
            setConversations((prev) => ({
                ...prev,
                [activeConversationId]: {
                    ...prev[activeConversationId],
                    messages: [
                        ...updatedMessages,
                        { role: 'assistant', content: 'Failed to process image. Please try again.' },
                    ],
                },
            }));
        } finally {
            setIsLoading(false);
        }
    };

    const handleLogin = (userInfo) => {
        setUser(userInfo);
        // Create initial conversation with timestamp
        const initialConvId = `conv_${Date.now()}`;
        const now = new Date();
        setConversations({
            [initialConvId]: {
                title: 'New Chat',
                timestamp: now,
                createdAt: now.toISOString(),
                messages: [
                    {
                        role: 'assistant',
                        content: `Hi ${userInfo.full_name}! How can I help you today?`,
                    },
                ],
            },
        });
        setActiveConversationId(initialConvId);
    };

    const handleLogout = () => {
        setUser(null);
        setConversations({});
        setActiveConversationId(null);
        setOrders([]);
    };

    const createNewConversation = () => {
        const newConvId = `conv_${Date.now()}`;
        const now = new Date();
        setConversations({
            ...conversations,
            [newConvId]: {
                title: 'New Chat',
                timestamp: now,
                createdAt: now.toISOString(),
                messages: [
                    {
                        role: 'assistant',
                        content: 'Hi! How can I help you today?',
                    },
                ],
            },
        });
        setActiveConversationId(newConvId);
        setSidebarOpen(false);
    };

    const switchConversation = (convId) => {
        setActiveConversationId(convId);
        setSidebarOpen(false);
    };

    const updateConversationTitle = async (convId, messages) => {
        const userMessageCount = messages.filter(m => m.role === 'user').length;

        // Update title after 2nd user message
        if (userMessageCount === 2) {
            const newTitle = await generateSmartTitle(messages);
            setConversations(prev => ({
                ...prev,
                [convId]: {
                    ...prev[convId],
                    title: newTitle,
                },
            }));
        }
    };

    const sendMessage = async (e) => {
        e.preventDefault();
        if (!inputValue.trim() || isLoading || !activeConversationId) return;

        const userMessage = inputValue.trim();
        setInputValue('');

        // Add user message to current conversation
        const updatedMessages = [...currentMessages, { role: 'user', content: userMessage }];

        setConversations({
            ...conversations,
            [activeConversationId]: {
                ...conversations[activeConversationId],
                messages: updatedMessages,
            },
        });

        setIsLoading(true);

        try {
            const response = await fetch(`${API_URL}/chat/message`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: userMessage,
                    user_id: user.email,
                    user_name: user.full_name,
                    email: user.email,
                }),
            });

            if (response.ok) {
                const data = await response.json();
                const finalMessages = [...updatedMessages, { role: 'assistant', content: data.response }];

                setConversations((prev) => ({
                    ...prev,
                    [activeConversationId]: {
                        ...prev[activeConversationId],
                        messages: finalMessages,
                    },
                }));

                // Update title after 2nd user message
                await updateConversationTitle(activeConversationId, finalMessages);
            } else {
                setConversations((prev) => ({
                    ...prev,
                    [activeConversationId]: {
                        ...prev[activeConversationId],
                        messages: [
                            ...updatedMessages,
                            { role: 'assistant', content: '' },
                        ],
                    },
                }));
            }
        } catch (error) {
            console.error('Error:', error);
            setConversations((prev) => ({
                ...prev,
                [activeConversationId]: {
                    ...prev[activeConversationId],
                    messages: [
                        ...updatedMessages,
                        { role: 'assistant', content: 'Connection error. Please check if the backend is running.' },
                    ],
                },
            }));
        } finally {
            setIsLoading(false);
        }
    };

    if (!user) {
        return <LoginForm onLogin={handleLogin} />;
    }

    // Sort conversations by timestamp (newest first)
    const sortedConversations = Object.entries(conversations).sort(
        ([, a], [, b]) => new Date(b.timestamp) - new Date(a.timestamp)
    );

    return (
        <main className={styles.chatContainer}>
            {/* Sidebar */}
            <div className={`${styles.sidebar} ${sidebarOpen ? styles.sidebarOpen : ''}`}>
                <div className={styles.sidebarHeader}>
                    <h2 className={styles.sidebarTitle}>Hello, {user.full_name}! 👋</h2>
                    <button onClick={handleLogout} className={styles.logoutButton}>
                        Sign Out
                    </button>
                </div>

                <button onClick={createNewConversation} className={styles.newConversationButton}>
                    ➕ New Conversation
                </button>

                {/* My Orders Section */}
                <div className={styles.ordersSection}>
                    <h3 className={styles.sectionTitle}>📦 My Orders</h3>
                    {orders.length > 0 ? (
                        <div className={styles.ordersList}>
                            {orders.map((order) => (
                                <button
                                    key={order.id}
                                    onClick={() => setSelectedOrder(order)}
                                    className={styles.orderItem}
                                >
                                    <div className={styles.orderName}>{order.item}</div>
                                    <div className={styles.orderStatus}>
                                        <span className={`${styles.statusBadge} ${styles[order.status.toLowerCase()]}`}>
                                            {order.status}
                                        </span>
                                        <span className={styles.orderDate}>{order.date}</span>
                                    </div>
                                </button>
                            ))}
                        </div>
                    ) : (
                        <p className={styles.emptyState}>No orders yet</p>
                    )}
                </div>

                {/* Conversations List */}
                <div className={styles.conversationList}>
                    <h3 className={styles.sectionTitle}>💬 Conversations</h3>
                    {sortedConversations.map(([convId, conv]) => (
                        <button
                            key={convId}
                            onClick={() => switchConversation(convId)}
                            className={`${styles.conversationItem} ${convId === activeConversationId ? styles.conversationItemActive : ''
                                }`}
                        >
                            <div className={styles.conversationTitle}>{conv.title}</div>
                            <div className={styles.conversationTime}>{formatTimestamp(new Date(conv.timestamp))}</div>
                        </button>
                    ))}
                </div>
            </div>

            {/* Mobile sidebar toggle */}
            <button className={styles.sidebarToggle} onClick={() => setSidebarOpen(!sidebarOpen)}>
                {sidebarOpen ? '✕' : '☰'}
            </button>

            {/* Main chat area */}
            <div className={styles.chatWindow}>
                <div className={styles.header}>
                    <h1 className={styles.title}>🛍️ ShopBuddy</h1>
                </div>

                <div className={styles.messagesContainer}>
                    {currentMessages.map((msg, index) => (
                        <ChatMessage key={index} message={msg} />
                    ))}
                    {isLoading && (
                        <div className={styles.loadingContainer}>
                            <div className={styles.loadingDots}>
                                <span></span>
                                <span></span>
                                <span></span>
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                <form onSubmit={sendMessage} className={styles.inputContainer}>
                    <input
                        type="file"
                        id="image-upload"
                        className={styles.hiddenInput}
                        accept="image/*"
                        onChange={handleImageUpload}
                        disabled={isLoading}
                        style={{ display: 'none' }}
                    />
                    <button
                        type="button"
                        onClick={() => document.getElementById('image-upload').click()}
                        className={styles.uploadButton}
                        disabled={isLoading}
                        title="Upload image for visual search"
                    >
                        📷
                    </button>
                    <input
                        type="text"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        placeholder="Ask about clothes, orders, or upload an image..."
                        className={styles.input}
                        disabled={isLoading}
                    />
                    <button type="submit" className={styles.sendButton} disabled={isLoading}>
                        Send
                    </button>
                </form>
            </div>

            {/* Order Details Modal */}
            {selectedOrder && (
                <OrderDetails
                    order={selectedOrder}
                    onClose={() => setSelectedOrder(null)}
                    onCancel={handleCancelOrder}
                />
            )}
        </main>
    );
}
