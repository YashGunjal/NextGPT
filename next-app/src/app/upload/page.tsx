"use client";
import { api } from "@/trpc/react";
import Link from "next/link";
// Import React and React Dropzone
import React from "react";
import { useUser } from "@clerk/nextjs";
import { useDropzone } from "react-dropzone";

type presignedPostOut = { 
    url: string;
    key: string;
}


export default function FileUploadComponent() {
  const { user } = useUser();
  console.log(user)
  const { getRootProps, getInputProps, acceptedFiles } = useDropzone({ multiple: false, maxSize:20000000, 
    onDropRejected: () => {
    alert('Maximum file upload size is 10MB');
  } });
  const getPresignedPost = api.file.getSignedUrl.useMutation();

  const handleSubmit = async (event: React.MouseEvent<HTMLButtonElement>) => {
    event.preventDefault();
    // console.log(encodeURIComponent(acceptedFiles[0].type);

    if (acceptedFiles[0]){
      const actual = user?.primaryEmailAddress?.emailAddress
      const uploadFolder =  (actual) ? actual : (user?.externalAccounts[0]?.emailAddress)  ? user?.externalAccounts[0]?.emailAddress : "yashgunjal98@gmail.com";
      const presignedPost = await getPresignedPost.mutateAsync({name : acceptedFiles[0].name, type: acceptedFiles[0].type, folder: uploadFolder});
      console.log("presignedPost", presignedPost); 
      console.log("url", presignedPost);
      
      const formData = new FormData();
      acceptedFiles.forEach(file => {
        formData.append('files', file);
      });
      console.log("formData",  formData)
      
      if (presignedPost !== null&& acceptedFiles.length > 0){
        const { url, key } = presignedPost as unknown as presignedPostOut
        
        const response = await fetch(url, {
          method: "PUT",
          body: formData,
        });
        console.log("response", response)
        
        if (response.status === 200) {
          console.log("File uploaded successfully!");
        } else {
          console.error("File upload failed!");
        }
      }
      else{
        alert("Please select a file to upload");
      }
      
    }
    console.log("Submitting files:", acceptedFiles);

  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-b from-[#2e026d] to-[#15162c] text-white">
      <div className="container flex flex-col items-center justify-center gap-12 px-4 py-16 ">
        <h1 className="p-4">Files Upload</h1>
        <div
          {...getRootProps({ className: "dropzone" })}
          style={{
            border: "2px dashed #007bff",
            padding: "20px",
            cursor: "pointer",
          }}
        >
          <input {...getInputProps()}/>
          <p>{"Drag 'n' drop some files here, or click to select files"}</p>
        </div>
        <ul className="p-4">
          {acceptedFiles.map((file, index) => (
            <li key={index}>{file.name}</li>
          ))}
        </ul>
        <button
          className="rounded border-blue-500 bg-white p-4 py-2 font-bold text-slate-700 hover:bg-slate-200 "
          onClick={handleSubmit}
        >
          Submit/Upload Files
        </button>
      </div>
      <Link href="/chat"> Back to Chat</Link>
    </main>
  );
}
