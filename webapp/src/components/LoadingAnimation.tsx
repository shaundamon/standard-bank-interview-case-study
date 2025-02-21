import React from 'react';
import { motion } from 'framer-motion';

const sampleImages = [
  'https://images.unsplash.com/photo-1579353977828-2a4eab540b9a', 
  'https://images.unsplash.com/photo-1579546929518-9e396f3cc809', 
  'https://images.unsplash.com/photo-1557672172-298e090bd0f1', 
  'https://images.unsplash.com/photo-1550859492-d5da9d8e45f3', 
  'https://images.unsplash.com/photo-1579546929662-711aa81148cf', 
  'https://images.unsplash.com/photo-1558591710-4b4a1ae0f04d', 
];

export const LoadingAnimation: React.FC = () => {
  return (
    <div className="relative h-64 w-full overflow-hidden rounded-lg mt-6">
      <div className="absolute inset-0 bg-gradient-to-r from-indigo-500/20 to-purple-500/20 backdrop-blur-sm" />
      {sampleImages.map((src, index) => (
        <motion.div
          key={src}
          className="absolute w-32 h-32 rounded-lg overflow-hidden"
          style={{
            left: '50%',
            top: '50%',
            x: '-50%',
            y: '-50%'
          }}
          initial={{ 
            opacity: 0,
            scale: 0.5,
          }}
          animate={{
            x: [
              `calc(-50% + ${Math.random() * 200 - 100}px)`,
              `calc(-50% + ${Math.random() * 200 - 100}px)`,
              `calc(-50% + ${Math.random() * 200 - 100}px)`
            ],
            y: [
              `calc(-50% + ${Math.random() * 150 - 75}px)`,
              `calc(-50% + ${Math.random() * 150 - 75}px)`,
              `calc(-50% + ${Math.random() * 150 - 75}px)`
            ],
            opacity: [0, 0.8, 0],
            scale: [0.5, 0.8, 0.5],
          }}
          transition={{
            duration: 1.5,
            repeat: Infinity,
            delay: index * 0.4,
            times: [0, 0.5, 1],
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
          animate={{ opacity: [0.6, 1, 0.6] }}
          transition={{ duration: 1, repeat: Infinity }}
        >
          Searching for images...
        </motion.div>
      </div>
    </div>
  );
};