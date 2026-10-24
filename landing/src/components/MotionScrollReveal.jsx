import React from 'react';
import { motion } from 'framer-motion';

/**
 * Sequential Scroll Reveal ("Presentation Slide" Entry)
 * Trigger: Entering viewport (whileInView, viewport: { once: true, margin: "-100px" })
 * Transform: Elements travel from opacity: 0, y: 28px to opacity: 1, y: 0
 * Easing: cubic-bezier(0.16, 1, 0.3, 1)
 */
export const editorialEase = [0.16, 1, 0.3, 1];

export function MotionSlideEntry({ children, delay = 0, className = "" }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 28 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-100px" }}
      transition={{
        duration: 0.65,
        delay,
        ease: editorialEase,
      }}
      className={className}
    >
      {children}
    </motion.div>
  );
}

export function MotionStaggerContainer({ children, className = "", staggerDelay = 0.08 }) {
  return (
    <motion.div
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, margin: "-100px" }}
      variants={{
        hidden: {},
        visible: {
          transition: {
            staggerChildren: staggerDelay,
          },
        },
      }}
      className={className}
    >
      {children}
    </motion.div>
  );
}

export function MotionStaggerItem({ children, className = "" }) {
  return (
    <motion.div
      variants={{
        hidden: { opacity: 0, y: 28 },
        visible: {
          opacity: 1,
          y: 0,
          transition: {
            duration: 0.65,
            ease: editorialEase,
          },
        },
      }}
      className={className}
    >
      {children}
    </motion.div>
  );
}
