'use client';

import styles from './OrderDetails.module.css';

export default function OrderDetails({ order, onClose, onCancel }) {
    const canCancel = order.status === 'Processing' || order.status === 'Pending';

    const handleCancel = () => {
        if (window.confirm(`Are you sure you want to cancel the order for "${order.item}"?`)) {
            onCancel(order.id);
        }
    };

    return (
        <div className={styles.overlay} onClick={onClose}>
            <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
                <div className={styles.header}>
                    <h2 className={styles.title}>Order Details</h2>
                    <button onClick={onClose} className={styles.closeButton}>✕</button>
                </div>

                <div className={styles.content}>
                    <div className={styles.orderInfo}>
                        <h3 className={styles.itemName}>{order.item}</h3>

                        <div className={styles.detailRow}>
                            <span className={styles.label}>Order ID:</span>
                            <span className={styles.value}>#{order.id}</span>
                        </div>

                        <div className={styles.detailRow}>
                            <span className={styles.label}>Order Date:</span>
                            <span className={styles.value}>{order.date}</span>
                        </div>

                        <div className={styles.detailRow}>
                            <span className={styles.label}>Status:</span>
                            <span className={`${styles.statusBadge} ${styles[order.status.toLowerCase()]}`}>
                                {order.status}
                            </span>
                        </div>

                        {order.price && (
                            <div className={styles.detailRow}>
                                <span className={styles.label}>Price:</span>
                                <span className={styles.value}>${order.price}</span>
                            </div>
                        )}

                        {order.quantity && (
                            <div className={styles.detailRow}>
                                <span className={styles.label}>Quantity:</span>
                                <span className={styles.value}>{order.quantity}</span>
                            </div>
                        )}

                        {order.trackingNumber && (
                            <div className={styles.detailRow}>
                                <span className={styles.label}>Tracking:</span>
                                <span className={styles.value}>{order.trackingNumber}</span>
                            </div>
                        )}

                        {order.estimatedDelivery && (
                            <div className={styles.detailRow}>
                                <span className={styles.label}>Est. Delivery:</span>
                                <span className={styles.value}>{order.estimatedDelivery}</span>
                            </div>
                        )}
                    </div>

                    <div className={styles.actions}>
                        {canCancel && (
                            <button onClick={handleCancel} className={styles.cancelButton}>
                                Cancel Order
                            </button>
                        )}
                        <button onClick={onClose} className={styles.closeActionButton}>
                            Close
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
