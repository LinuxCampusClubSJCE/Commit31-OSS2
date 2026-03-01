import { useState, useEffect, useCallback } from 'react'
import axios from 'axios'
import './SnapshotManager.css'

interface Snapshot {
  id: string
  sessionId: string
  name: string
  description: string
  createdAt: string
  containerId: string | null
  osType: string | null
}

interface SnapshotManagerProps {
  sessionId: string
  isOpen: boolean
  onClose: () => void
}

type NotificationType = 'success' | 'error'

interface Notification {
  message: string
  type: NotificationType
}

function SnapshotManager({ sessionId, isOpen, onClose }: SnapshotManagerProps) {
  const [snapshots, setSnapshots] = useState<Snapshot[]>([])
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [loading, setLoading] = useState(false)
  const [savingNew, setSavingNew] = useState(false)
  const [restoringId, setRestoringId] = useState<string | null>(null)
  const [notification, setNotification] = useState<Notification | null>(null)

  const notify = useCallback((message: string, type: NotificationType) => {
    setNotification({ message, type })
    setTimeout(() => setNotification(null), 3500)
  }, [])

  const fetchSnapshots = useCallback(async () => {
    setLoading(true)
    try {
      const res = await axios.get(`/api/sessions/${sessionId}/snapshots`)
      if (res.data.success) {
        setSnapshots(res.data.snapshots)
      }
    } catch {
      notify('Failed to load snapshots', 'error')
    } finally {
      setLoading(false)
    }
  }, [sessionId, notify])

  useEffect(() => {
    if (isOpen) fetchSnapshots()
  }, [isOpen, fetchSnapshots])

  const handleSave = async () => {
    if (!name.trim()) {
      notify('Please enter a snapshot name', 'error')
      return
    }
    setSavingNew(true)
    try {
      const res = await axios.post(`/api/sessions/${sessionId}/snapshots`, {
        name: name.trim(),
        description: description.trim(),
      })
      if (res.data.success) {
        setSnapshots(prev => [res.data.snapshot, ...prev])
        setName('')
        setDescription('')
        notify(`Snapshot "${res.data.snapshot.name}" saved`, 'success')
      }
    } catch {
      notify('Failed to save snapshot', 'error')
    } finally {
      setSavingNew(false)
    }
  }

  const handleRestore = async (snapshot: Snapshot) => {
    setRestoringId(snapshot.id)
    try {
      const res = await axios.post(
        `/api/sessions/${sessionId}/snapshots/${snapshot.id}/restore`
      )
      if (res.data.success) {
        notify(`Restored "${snapshot.name}" successfully`, 'success')
      }
    } catch {
      notify(`Failed to restore "${snapshot.name}"`, 'error')
    } finally {
      setRestoringId(null)
    }
  }

  const formatDate = (iso: string) => {
    const d = new Date(iso)
    return d.toLocaleDateString(undefined, {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  if (!isOpen) return null

  return (
    <div className="snapshot-overlay" onClick={onClose}>
      <div className="snapshot-modal" onClick={e => e.stopPropagation()}>
        {notification && (
          <div className={`snapshot-toast snapshot-toast--${notification.type}`}>
            {notification.type === 'success' ? '✓' : '✕'} {notification.message}
          </div>
        )}

        <div className="snapshot-modal-header">
          <h3>Snapshot Manager</h3>
          <button className="snapshot-close-btn" onClick={onClose}>
            ×
          </button>
        </div>

        <div className="snapshot-modal-body">
          <div className="snapshot-create-section">
            <h4>Save Current Workspace</h4>
            <input
              type="text"
              className="snapshot-input"
              placeholder="Snapshot name"
              value={name}
              onChange={e => setName(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && handleSave()}
              disabled={savingNew}
            />
            <textarea
              className="snapshot-input snapshot-textarea"
              placeholder="Description (optional)"
              value={description}
              onChange={e => setDescription(e.target.value)}
              rows={2}
              disabled={savingNew}
            />
            <button
              className="snapshot-save-btn"
              onClick={handleSave}
              disabled={savingNew || !name.trim()}
            >
              {savingNew ? (
                <span className="snapshot-spinner" />
              ) : (
                '💾'
              )}{' '}
              {savingNew ? 'Saving...' : 'Save Snapshot'}
            </button>
          </div>

          <div className="snapshot-divider" />

          <div className="snapshot-list-section">
            <h4>
              Saved Snapshots
              {!loading && <span className="snapshot-count">{snapshots.length}</span>}
            </h4>

            {loading ? (
              <div className="snapshot-loading">
                <span className="snapshot-spinner snapshot-spinner--lg" />
                <span>Loading snapshots...</span>
              </div>
            ) : snapshots.length === 0 ? (
              <div className="snapshot-empty">
                No snapshots yet. Save your first one above.
              </div>
            ) : (
              <ul className="snapshot-items">
                {snapshots.map(s => (
                  <li key={s.id} className="snapshot-item">
                    <div className="snapshot-item-info">
                      <span className="snapshot-item-name">{s.name}</span>
                      <span className="snapshot-item-date">
                        {s.createdAt ? formatDate(s.createdAt) : '—'}
                      </span>
                      {s.description && (
                        <span className="snapshot-item-desc">{s.description}</span>
                      )}
                      {s.osType && (
                        <span className="snapshot-item-os">{s.osType}</span>
                      )}
                    </div>
                    <button
                      className="snapshot-restore-btn"
                      onClick={() => handleRestore(s)}
                      disabled={restoringId === s.id}
                    >
                      {restoringId === s.id ? (
                        <span className="snapshot-spinner" />
                      ) : (
                        '⏮'
                      )}{' '}
                      {restoringId === s.id ? 'Restoring...' : 'Restore'}
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default SnapshotManager
