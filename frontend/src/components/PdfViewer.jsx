import { Viewer, Worker } from "@react-pdf-viewer/core";
import { toolbarPlugin } from "@react-pdf-viewer/toolbar";

import "@react-pdf-viewer/core/lib/styles/index.css";
import "@react-pdf-viewer/default-layout/lib/styles/index.css";
import "@react-pdf-viewer/toolbar/lib/styles/index.css";

const PdfViewer = ({ file }) => {
  const toolbarPluginInstance = toolbarPlugin();
  const { renderDefaultToolbar, Toolbar } = toolbarPluginInstance;

  const transform = (slot) => ({
    ...slot,
    // These slots will be empty
    Open: () => <></>,
    SwitchTheme: () => <></>,
  });

  return (
    <Worker workerUrl="https://unpkg.com/pdfjs-dist@2.16.105/build/pdf.worker.js">
      <div
        style={{ display: "flex", flexDirection: "column", height: "100vh" }}
      >
        <div className="bg-white">
          <Toolbar>{renderDefaultToolbar(transform)}</Toolbar>
        </div>
        <div style={{ flex: 1, overflow: "hidden" }}>
          <Viewer
            fileUrl={file}
            plugins={[toolbarPluginInstance]}
            // theme="dark"
          />
        </div>
      </div>
    </Worker>
  );
};

export default PdfViewer;
