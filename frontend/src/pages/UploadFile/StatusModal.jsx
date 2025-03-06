import React from "react";

const StatusModal = ({ status, loading }) => {
  return (
    <div>
      <div className="bg-gray-900 absolute inset-0 z-50 backdrop-filter backdrop-blur-lg opacity-80"></div>
      <div className=" absolute inset-0 flex items-center justify-center z-50">
        {loading ? (
          <div className="bg-white h-auto p-12 text-center flex flex-row gap-4 items-center rounded-md">
            <div className="loader w-16 h-16 border-t-4 border-b-4 border-blue-500 border-solid rounded-full animate-spin"></div>

            <h1 className="font-bold text-2xl text-teal-500 ">{status}</h1>
          </div>
        ) : (
          ""
        )}
      </div>
    </div>
  );
};

export default StatusModal;
