import { DataSection } from './components/DataSection';
import { motion } from 'motion/react';

export default function App() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Header */}
      <motion.header 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="sticky top-0 z-50 bg-background/80 backdrop-blur-md border-b border-border"
      >
        <div className="max-w-6xl mx-auto px-6 py-6">
          <h1>Data Analysis Project</h1>
          <p className="text-muted-foreground mt-2">
            Comprehensive insights and conclusions from our research
          </p>
        </div>
      </motion.header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-6 py-12">
        <DataSection
          sectionNumber={1}
          title="Market Trends Analysis"
          conclusion="Our analysis reveals a significant upward trend in market adoption over the past 18 months. The data shows a 34% increase in user engagement, with peak activity occurring during Q3 2024. This growth pattern suggests strong market validation and indicates potential for sustained expansion in the coming quarters."
          graphPlaceholder="market-trends"
          delay={0.2}
        />

        <DataSection
          sectionNumber={2}
          title="User Behavior Patterns"
          conclusion="User session data indicates a clear preference for mobile interactions, accounting for 67% of total traffic. Average session duration increased by 2.3 minutes, and bounce rates decreased by 15%. These metrics suggest improved user experience and content relevance across all platforms."
          graphPlaceholder="user-behavior"
          delay={0.3}
          reversed
        />

        <DataSection
          sectionNumber={3}
          title="Revenue Distribution"
          conclusion="Revenue streams show healthy diversification with subscription services contributing 52%, one-time purchases at 31%, and partnerships at 17%. The subscription model demonstrates strong retention rates at 89%, indicating high customer satisfaction and product-market fit."
          graphPlaceholder="revenue-chart"
          delay={0.4}
        />

        <DataSection
          sectionNumber={4}
          title="Geographic Expansion"
          conclusion="Geographic analysis reveals strong performance in established markets while showing promising growth in emerging regions. North America maintains 45% of total market share, followed by Europe at 30% and Asia-Pacific showing rapid growth at 18% year-over-year. This distribution supports our multi-regional expansion strategy."
          graphPlaceholder="geographic-data"
          delay={0.5}
          reversed
        />

        <DataSection
          sectionNumber={5}
          title="Performance Metrics"
          conclusion="System performance metrics exceed industry benchmarks with 99.8% uptime, average response times under 200ms, and successful request rates at 99.95%. These technical achievements directly correlate with improved user satisfaction scores and reduced churn rates."
          graphPlaceholder="performance-metrics"
          delay={0.6}
        />

        <DataSection
          sectionNumber={6}
          title="Future Projections"
          conclusion="Predictive modeling based on historical data and current trajectories suggests continued growth with conservative estimates indicating 25-30% expansion over the next 12 months. Key drivers include product enhancements, market expansion initiatives, and strategic partnerships currently in development."
          graphPlaceholder="future-forecast"
          delay={0.7}
          reversed
        />
      </main>

      {/* Footer */}
      <footer className="border-t border-border mt-24">
        <div className="max-w-6xl mx-auto px-6 py-8">
          <p className="text-muted-foreground text-center">
            Data Analysis Project © 2025 | All conclusions based on comprehensive data analysis
          </p>
        </div>
      </footer>
    </div>
  );
}
