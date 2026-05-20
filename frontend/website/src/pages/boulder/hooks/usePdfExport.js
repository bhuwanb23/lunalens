import { useState, useCallback } from 'react';
import { PDF_EXPORT_CONFIG, PDF_SECTIONS, PDF_TEMPLATES, PDF_STYLES, PDF_LAYOUTS } from '../constants/pdfExport';

export const usePdfExport = () => {
  const [isExporting, setIsExporting] = useState(false);
  const [exportProgress, setExportProgress] = useState(0);

  const generatePdfReport = useCallback(async (analysisResults) => {
    setIsExporting(true);
    setExportProgress(0);

    try {
      // Create HTML content for PDF
      const htmlContent = generateHtmlReport(analysisResults);
      setExportProgress(50);

      // Convert HTML to PDF using browser's print functionality
      const result = await convertHtmlToPdf(htmlContent);
      setExportProgress(100);

      return { success: true, filename: result.filename };
    } catch (error) {
      console.error('PDF generation error:', error);
      return { success: false, error: error.message };
    } finally {
      setIsExporting(false);
      setExportProgress(0);
    }
  }, []);

  const generateHtmlReport = (analysisResults) => {
    const date = new Date().toLocaleDateString();
    const time = new Date().toLocaleTimeString();

    return `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <title>LunaLens Boulder Detection Report</title>
        <style>
          @media print {
            body { margin: 0; }
            .section { page-break-inside: avoid; }
            .page-break { page-break-before: always; }
          }
          body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 20px;
            background: white;
            color: #1f2937;
            line-height: 1.6;
          }
          .header {
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #3b82f6;
            padding-bottom: 20px;
          }
          .logo {
            font-size: 48px;
            margin-bottom: 10px;
          }
          .title {
            font-size: 24px;
            font-weight: bold;
            color: #1f2937;
            margin-bottom: 5px;
          }
          .subtitle {
            font-size: 16px;
            color: #6b7280;
            margin-bottom: 20px;
          }
          .section {
            margin-bottom: 25px;
            page-break-inside: avoid;
          }
          .section-title {
            font-size: 18px;
            font-weight: bold;
            color: #3b82f6;
            margin-bottom: 15px;
            border-left: 4px solid #3b82f6;
            padding-left: 10px;
          }
          .info-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 20px;
          }
          .info-item {
            background: #f9fafb;
            padding: 10px;
            border-radius: 5px;
            border-left: 3px solid #3b82f6;
          }
          .info-label {
            font-weight: bold;
            color: #374151;
            font-size: 12px;
            text-transform: uppercase;
          }
          .info-value {
            font-size: 14px;
            color: #1f2937;
            margin-top: 5px;
          }
          table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
            font-size: 12px;
          }
          th {
            background: #f3f4f6;
            padding: 10px;
            text-align: left;
            font-weight: bold;
            border: 1px solid #d1d5db;
          }
          td {
            padding: 8px 10px;
            border: 1px solid #d1d5db;
          }
          .object-card {
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
          }
          .object-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
          }
          .object-type {
            font-weight: bold;
            color: #3b82f6;
          }
          .confidence {
            background: #10b981;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 11px;
          }
          .measurements {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 10px;
            margin-top: 10px;
          }
          .measurement {
            text-align: center;
            padding: 5px;
            background: white;
            border-radius: 4px;
            border: 1px solid #e5e7eb;
          }
          .measurement-label {
            font-size: 10px;
            color: #6b7280;
            text-transform: uppercase;
          }
          .measurement-value {
            font-size: 12px;
            font-weight: bold;
            color: #1f2937;
            margin-top: 2px;
          }
          .footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
            font-size: 10px;
            color: #6b7280;
            text-align: center;
          }
        </style>
      </head>
      <body>
        <div class="header">
          <div class="logo">🌙</div>
          <div class="title">LunaLens Boulder Detection Report</div>
          <div class="subtitle">Advanced AI-Powered Lunar Surface Analysis</div>
          <div style="font-size: 12px; color: #6b7280;">
            Generated on ${date} at ${time}
          </div>
        </div>

        <div class="section">
          <div class="section-title">Executive Summary</div>
          <div class="info-grid">
            <div class="info-item">
              <div class="info-label">Analysis Type</div>
              <div class="info-value">${analysisResults.analysisType || 'Standard'}</div>
            </div>
            <div class="info-item">
              <div class="info-label">Total Objects</div>
              <div class="info-value">${analysisResults.totalObjects || 0}</div>
            </div>
            <div class="info-item">
              <div class="info-label">Boulders Detected</div>
              <div class="info-value">${analysisResults.boulders || 0}</div>
            </div>
            <div class="info-item">
              <div class="info-label">Craters Detected</div>
              <div class="info-value">${analysisResults.craters || 0}</div>
            </div>
            <div class="info-item">
              <div class="info-label">Average Confidence</div>
              <div class="info-value">${((analysisResults.confidence || 0) * 100).toFixed(1)}%</div>
            </div>
            <div class="info-item">
              <div class="info-label">Processing Time</div>
              <div class="info-value">${analysisResults.processingTime || 0}s</div>
            </div>
          </div>
        </div>

        <div class="section">
          <div class="section-title">Detection Results</div>
          ${generateDetectionResultsTable(analysisResults)}
        </div>

        <div class="section">
          <div class="section-title">Detailed Analysis</div>
          <div class="info-grid">
            <div class="info-item">
              <div class="info-label">Average Diameter</div>
              <div class="info-value">${(analysisResults.averageSize || 0).toFixed(2)}m</div>
            </div>
            <div class="info-item">
              <div class="info-label">Average Area</div>
              <div class="info-value">${(analysisResults.analysisSummary?.average_area || 0).toFixed(2)}m²</div>
            </div>
            <div class="info-item">
              <div class="info-label">Total Volume</div>
              <div class="info-value">${(analysisResults.analysisSummary?.total_volume || 0).toFixed(2)}m³</div>
            </div>
            <div class="info-item">
              <div class="info-label">Object Density</div>
              <div class="info-value">${(analysisResults.density || 0).toFixed(6)} obj/m²</div>
            </div>
            <div class="info-item">
              <div class="info-label">Average Circularity</div>
              <div class="info-value">${(analysisResults.analysisSummary?.average_circularity || 0).toFixed(3)}</div>
            </div>
            <div class="info-item">
              <div class="info-label">Average Elongation</div>
              <div class="info-value">${(analysisResults.analysisSummary?.average_elongation || 0).toFixed(3)}</div>
            </div>
          </div>
        </div>

        ${generateTechnicalDataSection(analysisResults)}

        ${generateDensityAnalysisSection(analysisResults)}

        <div class="section">
          <div class="section-title">Analysis Images</div>
          ${generateImagesSection(analysisResults)}
        </div>

        <div class="footer">
          <p>Generated by LunaLens AI System</p>
          <p>Report ID: ${Date.now()}</p>
          <p>All measurements are in meters unless otherwise specified</p>
        </div>
      </body>
      </html>
    `;
  };

  const generateDetectionResultsTable = (analysisResults) => {
    if (!analysisResults.detectedObjects || analysisResults.detectedObjects.length === 0) {
      return '<p>No objects detected in this analysis.</p>';
    }

    let tableHtml = `
      <table>
        <thead>
          <tr>
            <th>Object</th>
            <th>Type</th>
            <th>Confidence</th>
            <th>Diameter (m)</th>
            <th>Area (m²)</th>
            <th>Volume (m³)</th>
            <th>Circularity</th>
          </tr>
        </thead>
        <tbody>
    `;

    analysisResults.detectedObjects.forEach((obj, index) => {
      tableHtml += `
        <tr>
          <td>#${index + 1}</td>
          <td>${obj.class_name || 'Unknown'}</td>
          <td>${(obj.confidence * 100).toFixed(1)}%</td>
          <td>${obj.diameter_real?.toFixed(2) || '0.00'}</td>
          <td>${obj.area_real?.toFixed(2) || '0.00'}</td>
          <td>${obj.volume_real?.toFixed(2) || '0.00'}</td>
          <td>${obj.circularity?.toFixed(3) || '0.000'}</td>
        </tr>
      `;
    });

    tableHtml += '</tbody></table>';
    return tableHtml;
  };

  const generateTechnicalDataSection = (analysisResults) => {
    if (!analysisResults.detectedObjects || analysisResults.detectedObjects.length === 0) {
      return '';
    }

    let html = '<div class="section"><div class="section-title">Technical Data</div>';

    analysisResults.detectedObjects.forEach((obj, index) => {
      html += `
        <div class="object-card">
          <div class="object-header">
            <div class="object-type">${obj.class_name} #${index + 1}</div>
            <div class="confidence">${(obj.confidence * 100).toFixed(1)}%</div>
          </div>
          <div class="measurements">
            <div class="measurement">
              <div class="measurement-label">Diameter</div>
              <div class="measurement-value">${obj.diameter_real?.toFixed(2) || '0.00'}m</div>
            </div>
            <div class="measurement">
              <div class="measurement-label">Area</div>
              <div class="measurement-value">${obj.area_real?.toFixed(2) || '0.00'}m²</div>
            </div>
            <div class="measurement">
              <div class="measurement-label">Volume</div>
              <div class="measurement-value">${obj.volume_real?.toFixed(2) || '0.00'}m³</div>
            </div>
            <div class="measurement">
              <div class="measurement-label">Circularity</div>
              <div class="measurement-value">${obj.circularity?.toFixed(3) || '0.000'}</div>
            </div>
            <div class="measurement">
              <div class="measurement-label">Elongation</div>
              <div class="measurement-value">${obj.elongation?.toFixed(3) || '0.000'}</div>
            </div>
            <div class="measurement">
              <div class="measurement-label">Degradation</div>
              <div class="measurement-value">${obj.degradation_state || 'N/A'}</div>
            </div>
          </div>
          ${obj.bounding_box ? `
            <div style="margin-top: 10px; font-size: 11px; color: #6b7280;">
              Bounding Box: (${obj.bounding_box.x1}, ${obj.bounding_box.y1}) - (${obj.bounding_box.x2}, ${obj.bounding_box.y2})
            </div>
          ` : ''}
        </div>
      `;
    });

    html += '</div>';
    return html;
  };

  const generateDensityAnalysisSection = (analysisResults) => {
    if (!analysisResults.densityAnalysis) {
      return '';
    }

    return `
      <div class="section">
        <div class="section-title">Density Analysis</div>
        <div class="info-grid">
          <div class="info-item">
            <div class="info-label">Total Image Area</div>
            <div class="info-value">${(analysisResults.densityAnalysis.total_area || 0).toFixed(2)} m²</div>
          </div>
          <div class="info-item">
            <div class="info-label">Crater Density</div>
            <div class="info-value">${(analysisResults.densityAnalysis.crater_density || 0).toFixed(6)} craters/m²</div>
          </div>
          <div class="info-item">
            <div class="info-label">Boulder Density</div>
            <div class="info-value">${(analysisResults.densityAnalysis.boulder_density || 0).toFixed(6)} boulders/m²</div>
          </div>
          <div class="info-item">
            <div class="info-label">Overall Density</div>
            <div class="info-value">${(analysisResults.densityAnalysis.density || 0).toFixed(6)} objects/m²</div>
          </div>
        </div>
      </div>
    `;
  };

  const generateImagesSection = (analysisResults) => {
    let html = '';
    
    if (analysisResults.visualizationImage) {
      html += `
        <div style="text-align: center; margin: 20px 0;">
          <div style="font-size: 12px; color: #6b7280; margin-bottom: 10px;">Detection Visualization</div>
          <div style="color: #6b7280; font-size: 12px;">Image available in web interface</div>
        </div>
      `;
    }
    
    if (analysisResults.gradcamImage) {
      html += `
        <div style="text-align: center; margin: 20px 0;">
          <div style="font-size: 12px; color: #6b7280; margin-bottom: 10px;">Grad-CAM Visualization</div>
          <div style="color: #6b7280; font-size: 12px;">Image available in web interface</div>
        </div>
      `;
    }
    
    return html;
  };

  const convertHtmlToPdf = async (htmlContent) => {
    return new Promise((resolve, reject) => {
      try {
        // Create a blob URL for the HTML content
        const blob = new Blob([htmlContent], { type: 'text/html' });
        const url = URL.createObjectURL(blob);
        
        // Create a temporary iframe to render the HTML
        const iframe = document.createElement('iframe');
        iframe.style.display = 'none';
        iframe.src = url;
        document.body.appendChild(iframe);
        
        iframe.onload = () => {
          try {
            // Wait a bit for content to render
            setTimeout(() => {
              try {
                // Use html2pdf.js for PDF generation
                import('html2pdf.js').then((html2pdf) => {
                  const element = iframe.contentDocument.body;
                  
                  const opt = {
                    margin: [10, 10, 10, 10],
                    filename: `lunalens_report_${new Date().toISOString().split('T')[0]}.pdf`,
                    image: { type: 'jpeg', quality: 0.98 },
                    html2canvas: { 
                      scale: 2,
                      useCORS: true,
                      allowTaint: true
                    },
                    jsPDF: { 
                      unit: 'mm', 
                      format: 'a4', 
                      orientation: 'portrait' 
                    }
                  };
                  
                  html2pdf.default().set(opt).from(element).save().then(() => {
                    // Cleanup
                    document.body.removeChild(iframe);
                    URL.revokeObjectURL(url);
                    resolve({ filename: opt.filename });
                  }).catch((error) => {
                    // Fallback to print method if html2pdf fails
                    console.warn('html2pdf failed, falling back to print method:', error);
                    fallbackToPrintMethod(htmlContent, resolve, reject);
                  });
                }).catch(() => {
                  // If html2pdf is not available, use fallback
                  fallbackToPrintMethod(htmlContent, resolve, reject);
                });
              } catch {
                fallbackToPrintMethod(htmlContent, resolve, reject);
              }
            }, 1000);
          } catch {
            fallbackToPrintMethod(htmlContent, resolve, reject);
          }
        };
        
        iframe.onerror = () => {
          fallbackToPrintMethod(htmlContent, resolve, reject);
        };
      } catch {
        fallbackToPrintMethod(htmlContent, resolve, reject);
      }
    });
  };

  const fallbackToPrintMethod = (htmlContent, resolve, reject) => {
    try {
      // Create a new window with the HTML content
      const printWindow = window.open('', '_blank');
      printWindow.document.write(htmlContent);
      printWindow.document.close();
      
      // Wait for content to load
      printWindow.onload = () => {
        try {
          // Trigger print dialog
          printWindow.print();
          
          // Close the window after a delay
          setTimeout(() => {
            printWindow.close();
            resolve({ filename: `lunalens_report_${new Date().toISOString().split('T')[0]}.pdf` });
          }, 1000);
        } catch (error) {
          printWindow.close();
          reject(error);
        }
      };
      
      printWindow.onerror = () => {
        printWindow.close();
        reject(new Error('Failed to load PDF content'));
      };
    } catch (error) {
      reject(error);
    }
  };

  return {
    generatePdfReport,
    isExporting,
    exportProgress
  };
};