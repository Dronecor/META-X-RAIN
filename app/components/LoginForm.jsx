'use client';

import { useState } from 'react';
import styles from './LoginForm.module.css';

export default function LoginForm({ onLogin }) {
    const [formData, setFormData] = useState({
        full_name: '',
        email: '',
    });

    const handleSubmit = (e) => {
        e.preventDefault();
        if (formData.full_name && formData.email) {
            onLogin(formData);
        }
    };

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    return (
        <div className={styles.container}>
            <div className={styles.loginCard}>
                <div className={styles.header}>
                    <h1 className={styles.title}>🛍️ ShopBuddy</h1>
                    <p className={styles.subtitle}>Your AI Fashion Assistant</p>
                </div>

                <form onSubmit={handleSubmit} className={styles.form}>
                    <div className={styles.inputGroup}>
                        <label htmlFor="full_name" className={styles.label}>
                            Full Name
                        </label>
                        <input
                            type="text"
                            id="full_name"
                            name="full_name"
                            value={formData.full_name}
                            onChange={handleChange}
                            className={styles.input}
                            placeholder="Enter your name"
                            required
                        />
                    </div>

                    <div className={styles.inputGroup}>
                        <label htmlFor="email" className={styles.label}>
                            Email Address
                        </label>
                        <input
                            type="email"
                            id="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            className={styles.input}
                            placeholder="your@email.com"
                            required
                        />
                    </div>

                    <button type="submit" className={styles.submitButton}>
                        Start Shopping
                    </button>
                </form>

                <p className={styles.footer}>
                    Get personalized fashion recommendations powered by AI
                </p>
            </div>
        </div>
    );
}
