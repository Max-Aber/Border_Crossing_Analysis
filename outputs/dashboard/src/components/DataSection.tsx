import { motion } from 'motion/react';
import { Badge } from './ui/badge';

interface DataSectionProps {
  sectionNumber: number;
  title: string;
  conclusion: string;
  graphPlaceholder: string;
  delay?: number;
  reversed?: boolean;
}

export function DataSection({
  sectionNumber,
  title,
  conclusion,
  graphPlaceholder,
  delay = 0,
  reversed = false,
}: DataSectionProps) {
  return (
    <motion.section
      initial={{ opacity: 0, y: 40 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-100px" }}
      transition={{ duration: 0.7, delay }}
      className="mb-24 scroll-mt-24"
    >
      <div className={`grid md:grid-cols-2 gap-8 items-center ${reversed ? 'md:grid-flow-dense' : ''}`}>
        {/* Text Content */}
        <div className={reversed ? 'md:col-start-2' : ''}>
          <Badge variant="outline" className="mb-4">
            Section {sectionNumber}
          </Badge>
          <h2 className="mb-6">{title}</h2>
          <div className="space-y-4">
            <p className="text-muted-foreground leading-relaxed">
              {conclusion}
            </p>
          </div>
        </div>

        {/* Graph Placeholder */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: delay + 0.2 }}
          className={`${reversed ? 'md:col-start-1 md:row-start-1' : ''}`}
        >
          <div className="relative aspect-[4/3] bg-card border border-border rounded-xl overflow-hidden group hover:border-primary/50 transition-all duration-300">
            {/* Grid pattern background */}
            <div className="absolute inset-0 opacity-20">
              <svg className="w-full h-full" xmlns="http://www.w3.org/2000/svg">
                <defs>
                  <pattern id={`grid-${graphPlaceholder}`} width="20" height="20" patternUnits="userSpaceOnUse">
                    <path
                      d="M 20 0 L 0 0 0 20"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="0.5"
                      className="text-muted-foreground"
                    />
                  </pattern>
                </defs>
                <rect width="100%" height="100%" fill={`url(#grid-${graphPlaceholder})`} />
              </svg>
            </div>

            {/* Placeholder content */}
            <div className="absolute inset-0 flex items-center justify-center p-8">
              <div className="text-center">
                <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-primary/10 mb-4 group-hover:bg-primary/20 transition-colors duration-300">
                  <svg
                    className="w-8 h-8 text-primary"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                    />
                  </svg>
                </div>
                <p className="text-muted-foreground">
                  {title} Graph
                </p>
                <p className="text-muted-foreground/60 mt-1">
                  Placeholder for visualization
                </p>
              </div>
            </div>

            {/* Decorative gradient overlay */}
            <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
          </div>
        </motion.div>
      </div>
    </motion.section>
  );
}
