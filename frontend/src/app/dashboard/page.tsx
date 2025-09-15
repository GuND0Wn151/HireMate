export default function DashboardPage() {
      return (
            <div className="p-6 max-w-5xl mx-auto">
                  <h1 className="text-2xl font-semibold mb-4">Dashboard</h1>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <section className="border rounded-lg p-4">
                              <h2 className="font-medium mb-2">Resume Analysis</h2>
                              <p className="text-sm text-gray-600">Similarity score, ATS feedback will appear here.</p>
                        </section>
                        <section className="border rounded-lg p-4">
                              <h2 className="font-medium mb-2">Interview Questions</h2>
                              <p className="text-sm text-gray-600">Latest JD-specific questions will appear here.</p>
                        </section>
                        <section className="border rounded-lg p-4">
                              <h2 className="font-medium mb-2">Last Practice Problem</h2>
                              <p className="text-sm text-gray-600">Your recent DSA activity.</p>
                        </section>
                        <section className="border rounded-lg p-4">
                              <h2 className="font-medium mb-2">Applications Summary</h2>
                              <p className="text-sm text-gray-600">Recent application statuses.</p>
                        </section>
                  </div>
            </div>
      );
}


