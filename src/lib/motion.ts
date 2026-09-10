// Apple-style Spring Physics & Haptic Feedback System

import { Variants } from 'framer-motion';

// Spring presets matching Apple's HIG
export const springPresets = {
  // Quick, responsive tap feedback
  tap: {
    type: 'spring' as const,
    stiffness: 500,
    damping: 30,
    mass: 1,
    restDelta: 0.001,
  },
  
  // Smooth layout transitions
  layout: {
    type: 'spring' as const,
    stiffness: 400,
    damping: 30,
    mass: 1.5,
  },
  
  // Sheet/modal presentations
  sheet: {
    type: 'spring' as const,
    stiffness: 350,
    damping: 30,
    mass: 2,
  },
  
  // Soft, gentle animations
  soft: {
    type: 'spring' as const,
    stiffness: 300,
    damping: 25,
    mass: 1,
  },
};

// Apple-style timing functions
export const timingFunctions = {
  easeOut: 'cubic-bezier(0.33, 1, 0.68, 1)',
  easeIn: 'cubic-bezier(0.32, 0, 0.67, 0)',
  easeInOut: 'cubic-bezier(0.65, 0, 0.35, 1)',
  spring: 'cubic-bezier(0.175, 0.885, 0.32, 1.275)',
};

// Button press animation
export const buttonPress = {
  scale: 0.96,
  transition: {
    type: 'spring',
    stiffness: 500,
    damping: 30,
    mass: 1,
  },
};

// Card hover and press variants
export const cardVariants: Variants = {
  initial: {
    scale: 1,
    boxShadow: '0 4px 16px rgba(0, 0, 0, 0.4)',
  },
  hover: {
    scale: 1.02,
    boxShadow: '0 8px 32px rgba(0, 0, 0, 0.5)',
    transition: {
      type: 'spring',
      stiffness: 400,
      damping: 30,
      mass: 1,
    },
  },
  tap: {
    scale: 0.98,
    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.3)',
    transition: {
      type: 'spring',
      stiffness: 500,
      damping: 30,
      mass: 1,
    },
  },
};

// Spring-based scale variants for general use
export const springVariants: Variants = {
  initial: { scale: 1 },
  animate: { scale: 1 },
  hover: { 
    scale: 1.03,
    transition: springPresets.layout,
  },
  tap: { 
    scale: 0.97,
    transition: springPresets.tap,
  },
};

// Fade and slide variants
export const fadeSlideVariants: Variants = {
  hidden: {
    opacity: 0,
    y: 20,
  },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      type: 'spring',
      stiffness: 300,
      damping: 30,
      mass: 1,
    },
  },
  exit: {
    opacity: 0,
    y: -20,
    transition: {
      duration: 0.2,
    },
  },
};

// Stagger container for lists
export const staggerContainer = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.05,
      delayChildren: 0.1,
    },
  },
};

// Stagger item variant
export const staggerItem: Variants = {
  hidden: {
    opacity: 0,
    y: 20,
  },
  show: {
    opacity: 1,
    y: 0,
    transition: {
      type: 'spring',
      stiffness: 300,
      damping: 25,
    },
  },
};

// Haptic feedback patterns (for use with navigator.vibrate)
export const hapticPatterns = {
  // Light tap feedback
  light: [5],
  
  // Medium confirmation
  medium: [10],
  
  // Heavy action
  heavy: [20],
  
  // Success pattern
  success: [10, 5, 10],
  
  // Error pattern
  error: [20, 10, 20],
  
  // Double tap
  double: [10, 50, 10],
};

// Trigger haptic feedback
export function triggerHaptic(pattern: keyof typeof hapticPatterns = 'light') {
  if (typeof navigator !== 'undefined' && 'vibrate' in navigator) {
    try {
      navigator.vibrate(hapticPatterns[pattern]);
    } catch (e) {
      // Haptic feedback not supported or blocked
    }
  }
}

// Check if reduced motion is preferred
export function prefersReducedMotion(): boolean {
  if (typeof window !== 'undefined') {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }
  return false;
}

// Get appropriate animation config based on user preferences
export function getAnimationConfig(preset: keyof typeof springPresets = 'soft') {
  if (prefersReducedMotion()) {
    return {
      type: 'tween' as const,
      duration: 0.01,
    };
  }
  return springPresets[preset];
}

// Page transition variants
export const pageVariants: Variants = {
  initial: {
    opacity: 0,
    scale: 0.98,
  },
  animate: {
    opacity: 1,
    scale: 1,
    transition: {
      type: 'spring',
      stiffness: 350,
      damping: 30,
      mass: 2,
      duration: 0.4,
    },
  },
  exit: {
    opacity: 0,
    scale: 0.98,
    transition: {
      duration: 0.2,
    },
  },
};

// Modal/Sheet presentation variants
export const modalVariants: Variants = {
  hidden: {
    opacity: 0,
    scale: 0.95,
    y: 20,
  },
  visible: {
    opacity: 1,
    scale: 1,
    y: 0,
    transition: {
      type: 'spring',
      stiffness: 350,
      damping: 30,
      mass: 2,
    },
  },
  exit: {
    opacity: 0,
    scale: 0.95,
    y: 20,
    transition: {
      duration: 0.2,
    },
  },
};

// Icon rotation for toggles
export const iconRotation = {
  idle: { rotate: 0 },
  active: { 
    rotate: 180,
    transition: {
      type: 'spring',
      stiffness: 500,
      damping: 25,
    },
  },
};

// Progress bar fill animation
export const progressFill = {
  initial: { width: 0 },
  fill: (progress: number) => ({
    width: `${progress}%`,
    transition: {
      type: 'spring',
      stiffness: 100,
      damping: 20,
      duration: 0.5,
    },
  }),
};

// List reordering animation
export const listReorder = {
  initial: { opacity: 0, scale: 0.8 },
  animate: { 
    opacity: 1, 
    scale: 1,
    transition: springPresets.layout,
  },
  exit: { 
    opacity: 0, 
    scale: 0.8,
    transition: { duration: 0.2 },
  },
};

// Drag gesture constraints
export const dragConstraints = {
  x: [-20, 20],
  y: [-20, 20],
};

// Drag end spring back
export const dragEnd = {
  type: 'spring',
  stiffness: 400,
  damping: 30,
  mass: 1,
};
