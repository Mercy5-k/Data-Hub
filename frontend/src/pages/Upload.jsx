import UploadForm from '../components/UploadForm'

export default function Upload() {
  return (
    <div className="page">
      <UploadForm onSuccess={() => alert('Uploaded!')} />
    </div>
  )
}
