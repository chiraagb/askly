import { useState } from "react";

import { Viewer, Worker } from "@react-pdf-viewer/core";
import "@react-pdf-viewer/core/lib/styles/index.css";
// import "@react-pdf-viewer/default-layout/lib/styles/index.css";

const ViewPdf = (props) => {
  const [pdfFile, setPdfFile] = useState(props.file);
  return (
    <div className="w-full  h-screen">
      <div className="h-full">
        <Worker workerUrl="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.4.120/pdf.worker.min.js">
          {pdfFile && (
            <>
              <Viewer fileUrl={pdfFile} />
            </>
          )}
          {!pdfFile && <>No Pdf</>}
        </Worker>
      </div>
    </div>
  );
};

export default ViewPdf;
