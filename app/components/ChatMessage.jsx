'use client';

import Image from 'next/image';
import styles from './ChatMessage.module.css';

function parseProductRecommendation(content) {
    const productRegex = /\*\*(.+?)\*\*\s*\n\*(.+?)\*\s*\n(?:(.+?)\n)?!\[.+?\]\((.+?)\)/g;
    const products = [];
    let lastIndex = 0;
    const parts = [];

    let match;
    while ((match = productRegex.exec(content)) !== null) {
        if (match.index > lastIndex) {
            parts.push({
                type: 'text',
                content: content.substring(lastIndex, match.index),
            });
        }

        const [, productName, priceAndStock, description, imageUrl] = match;

        const priceMatch = priceAndStock.match(/[₦$](\d+)/);
        const price = priceMatch ? `₦${priceMatch[1]}` : '₦0';

        let stockStatus = 'In Stock';
        let stockIcon = '✓';
        if (priceAndStock.includes('Low Stock')) {
            stockStatus = 'Low Stock';
            stockIcon = '⚠️';
        } else if (priceAndStock.includes('Out of Stock')) {
            stockStatus = 'Out of Stock';
            stockIcon = '❌';
        }

        products.push({
            type: 'product',
            name: productName.trim(),
            price,
            stockStatus,
            stockIcon,
            description: description?.trim() || '',
            imageUrl: imageUrl.trim(),
        });

        parts.push(products[products.length - 1]);
        lastIndex = match.index + match[0].length;
    }

    if (lastIndex < content.length) {
        parts.push({
            type: 'text',
            content: content.substring(lastIndex),
        });
    }

    return parts.length > 0 ? parts : [{ type: 'text', content }];
}

function formatText(text) {
    text = text.replace(/---/g, '');

    const lines = text.split('\n').map((line) => {
        line = line.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
        line = line.replace(/\*(.+?)\*/g, '<em>$1</em>');
        return line;
    });

    return lines.join('<br />');
}

export default function ChatMessage({ message }) {
    const isUser = message.role === 'user';
    let parts = [];
    if (isUser) {
        if (message.image_url) {
            parts = [
                { type: 'text', content: message.content },
                {
                    type: 'product', // Reusing product type for convenient image rendering
                    name: 'Uploaded Image',
                    price: '', // No price
                    stockStatus: '',
                    stockIcon: '',
                    description: '',
                    imageUrl: message.image_url
                }
            ];
        } else {
            parts = [{ type: 'text', content: message.content }];
        }
    } else {
        parts = parseProductRecommendation(message.content);
    }

    return (
        <div className={`${styles.messageWrapper} ${isUser ? styles.userWrapper : styles.assistantWrapper}`}>
            <div className={`${styles.messageBubble} ${isUser ? styles.userBubble : styles.assistantBubble}`}>
                {parts.map((part, index) => {
                    if (part.type === 'text') {
                        const formattedText = formatText(part.content);
                        return formattedText.trim() ? (
                            <div
                                key={index}
                                className={styles.messageText}
                                dangerouslySetInnerHTML={{ __html: formattedText }}
                            />
                        ) : null;
                    }

                    if (part.type === 'product') {
                        return (
                            <div key={index} className={styles.productCard}>
                                <div className={styles.imageContainer}>
                                    <Image
                                        src={part.imageUrl}
                                        alt={part.name}
                                        width={200}
                                        height={300}
                                        className={styles.productImage}
                                        unoptimized
                                    />
                                </div>

                                <div className={styles.productInfo}>
                                    <h3 className={styles.productName}>{part.name}</h3>
                                    {part.description && (
                                        <p className={styles.productDescription}>{part.description}</p>
                                    )}
                                    <div className={styles.productMeta}>
                                        <span className={styles.price}>{part.price}</span>
                                        <span className={`${styles.stock} ${part.stockIcon === '❌' ? styles.outOfStock : ''}`}>
                                            {part.stockIcon} {part.stockStatus}
                                        </span>
                                    </div>
                                </div>
                            </div>
                        );
                    }

                    return null;
                })}
            </div>
        </div>
    );
}
