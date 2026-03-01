import { useEffect, useState } from 'react'
import { useParams, useLocation } from 'react-router-dom'
import Terminal from '../components/Terminal'
import CodeEditor from '../components/CodeEditor'
import FileExplorer from '../components/FileExplorer'
import VideoCall from '../components/VideoCall'
import AIAssistant from '../components/AIAssistant'
import SnapshotManager from '../components/SnapshotManager'
import { useSocket } from '../hooks/useSocket'
import './WorkspacePage.css'

function WorkspacePage() {
  const { sessionId } = useParams()
  const location = useLocation()
  const socket = useSocket(sessionId!)
  const [currentFile, setCurrentFile] = useState<string | null>(null)
  const [showTunnelUrl, setShowTunnelUrl] = useState(true)
  const [showSnapshots, setShowSnapshots] = useState(false)
  const tunnelUrl = location.state?.tunnelUrl

  useEffect(() => {
    if (socket) {
      console.log('Connected to session:', sessionId)
    }
  }, [socket, sessionId])

  const copyTunnelUrl = () => {
    if (tunnelUrl) {
      navigator.clipboard.writeText(tunnelUrl)
      alert('Tunnel URL copied to clipboard!')
    }
  }

  return (
    <div className="workspace-page">
      <header className="workspace-header">
        <h2>Ghost Labs - Session: {sessionId}</h2>
        <div className="header-actions">
          {tunnelUrl && showTunnelUrl && (
            <div className="tunnel-url-banner">
              <span className="tunnel-label">🌐 Share URL:</span>
              <code className="tunnel-url">{tunnelUrl}</code>
              <button className="btn-copy" onClick={copyTunnelUrl}>📋 Copy</button>
              <button className="btn-close" onClick={() => setShowTunnelUrl(false)}>×</button>
            </div>
          )}
          <button className="btn-icon" onClick={() => setShowSnapshots(true)}>💾 Snapshots</button>
          <button className="btn-icon" onClick={() => setShowTunnelUrl(true)}>📤 Share</button>
        </div>
      </header>

      <div className="workspace-layout">
        <div className="sidebar">
          <FileExplorer onFileSelect={setCurrentFile} />
        </div>

        <div className="main-content">
          <div className="editor-section">
            <CodeEditor file={currentFile} />
          </div>
          <div className="terminal-section">
            <Terminal />
          </div>
        </div>

        <div className="right-panel">
          <VideoCall sessionId={sessionId!} />
          <AIAssistant />
        </div>
      </div>

      <SnapshotManager
        sessionId={sessionId!}
        isOpen={showSnapshots}
        onClose={() => setShowSnapshots(false)}
      />
    </div>
  )
}

export default WorkspacePage
