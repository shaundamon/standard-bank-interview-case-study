import React from 'react';
import { motion } from 'framer-motion';

const sampleImages = [
  'https://images.unsplash.com/photo-1682687982501-1e58ab814714',
  'https://images.unsplash.com/photo-1682687218147-9c86b46b861b',
  'https://images.unsplash.com/photo-1706699931950-a5a696e0c1d2',
  'https://images.unsplash.com/photo-1682695796954-bad0d0468ac4',
];

export const LoadingAnimation: React.FC = () => {
  return (
    <div className="relative h-64 w-full overflow-hidden rounded-lg">
      <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/20 to-purple-500/20 backdrop-blur-sm" />
      {sampleImages.map((src, index) => (
        <motion.div
          key={src}
          className="absolute w-32 h-32 rounded-lg overflow-hidden"
          initial={{ 
            x: Math.random() * 400 - 200,
            y: Math.random() * 400 - 200,
            opacity: 0,
            scale: 0.5
          }}
          animate={{
            x: Math.random() * 400 - 200,
            y: Math.random() * 400 - 200,
            opacity: [0, 1, 1, 0],
            scale: [0.5, 1, 1, 0.5],
          }}
          transition={{
            duration: 3,
            repeat: Infinity,
            delay: index * 0.5,
            ease: "easeInOut"
          }}
        >
          <img
            src={src}
            alt="Loading animation"
            className="w-full h-full object-cover"
          />
        </motion.div>
      ))}
      <div className="absolute inset-0 flex items-center justify-center">
        <motion.div
          className="text-lg font-medium text-indigo-600 dark:text-indigo-400"
          animate={{ opacity: [0.5, 1, 0.5] }}
          transition={{ duration: 1.5, repeat: Infinity }}
        >
          Searching for images...
        </motion.div>
      </div>
    </div>
  );
};