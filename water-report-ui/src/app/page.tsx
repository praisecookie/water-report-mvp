import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import PdfButton from "@/components/PdfButton";

// 1. Fetch Function
async function getComplianceData() {
  // using 127.0.0.1 instead of localhost to prevent networking quirks on my Macs
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'}/api/compliance-summary`, { cache: 'no-store' });
  
  if (!res.ok) {
    throw new Error('Failed to fetch API data');
  }
  
  return res.json();
}

async function getTechnicianRoster() {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'}/api/technicians`, { cache: 'no-store' });
  
  if (!res.ok) {
    throw new Error('Failed to fetch roster data');
  }
  
  return res.json();
}

// 2. Dashboard View
export default async function Dashboard() {
  
  const data = await getComplianceData();
  const roster = await getTechnicianRoster();

  return (
    <main className="min-h-screen bg-slate-50 p-8 print:bg-white print:p-0">
      <div className="max-w-6xl mx-auto space-y-8">
        
        {/* Header Section */}
        <div className="flex justify-between items-end">
          <div>
            <h1 className="text-3xl font-bold text-slate-900">Workforce Readiness Report</h1>
            <p className="text-slate-500 mt-2">Live Compliance & Capacity Overview</p>
          </div>
          <div className="flex items-center gap-4">
            <Badge variant={data.compliance_rate_percentage >= 80 ? "default" : "destructive"} className="text-sm px-4 py-1 print:hidden">
              {data.compliance_rate_percentage >= 80 ? "System Healthy" : "Action Required"}
            </Badge>
            <PdfButton />
          </div>
        </div>

        {/* Top Row: Key Metrics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-slate-500">Total Certifications Tracked</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-bold text-slate-900">{data.total_certifications}</div>
              <p className="text-xs text-slate-500 mt-1">Across all workforce regions</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-slate-500">Active & Compliant</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-bold text-emerald-600">{data.active}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-slate-500">Expired (Risk Flag)</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-bold text-red-600">{data.expired}</div>
            </CardContent>
          </Card>

        </div>

        {/* Middle Row: Visual Progress Bar */}
        <Card className="bg-white">
          <CardHeader>
            <CardTitle>Global Compliance Rate: {data.compliance_rate_percentage}%</CardTitle>
          </CardHeader>
          <CardContent>
            <Progress value={data.compliance_rate_percentage} className="h-4 w-full" />
            <p className="text-sm text-slate-500 mt-4">
              Target compliance is 100%. Technicians with expired certifications cannot be legally scheduled for site visits.
            </p>
          </CardContent>
        </Card>

        {/* Bottom Section: The Actionable Roster */}
        <Card className="bg-white mt-8">
          <CardHeader>
            <CardTitle>Workforce Compliance Roster</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Technician Name</TableHead>
                  <TableHead>Role</TableHead>
                  <TableHead>Region</TableHead>
                  <TableHead className="text-right">Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {roster.map((tech: any) => (
                  <TableRow key={tech.id}>
                    <TableCell className="font-medium">{tech.name}</TableCell>
                    <TableCell>{tech.role}</TableCell>
                    <TableCell>{tech.region}</TableCell>
                    <TableCell className="text-right">
                      <Badge variant={tech.status === "Compliant" ? "default" : "destructive"}>
                        {tech.status}
                      </Badge>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>

      </div>
    </main>
  );
}