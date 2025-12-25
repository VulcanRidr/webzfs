"""
Custom exceptions for the webzfs application

This module defines custom exceptions used in the application to handle specific error
conditions in ZFS operations, SMART monitoring, and system interactions. 
These exceptions provide:
- Clear error categorization for better error handling and debugging
- Consistent error reporting across the application
- Specific exception types for each operation type (pools, datasets, snapshots, etc.)
- Context-aware error messages with command and return code information
"""


class ProcessError(Exception):
    """Base exception for process errors"""
    pass


class ZFSException(Exception):
    """Base exception for all ZFS operations"""
    
    def __init__(self, message: str, command: str = None, return_code: int = None):
        self.message = message
        self.command = command
        self.return_code = return_code
        super().__init__(self.message)
    
    def __str__(self):
        if self.command:
            return f"{self.message} (Command: {self.command}, Exit Code: {self.return_code})"
        return self.message


class ZFSPoolException(ZFSException):
    """Base exception for ZFS pool operations"""
    pass


class PoolNotFoundException(ZFSPoolException):
    """Raised when a specified pool is not found"""
    pass


class PoolAlreadyExistsException(ZFSPoolException):
    """Raised when trying to create a pool that already exists"""
    pass


class PoolCreationException(ZFSPoolException):
    """Raised when pool creation fails"""
    pass


class PoolDestructionException(ZFSPoolException):
    """Raised when pool destruction fails"""
    pass


class PoolImportException(ZFSPoolException):
    """Raised when pool import fails"""
    pass


class PoolExportException(ZFSPoolException):
    """Raised when pool export fails"""
    pass


class PoolHealthException(ZFSPoolException):
    """Raised when pool health status is critical"""
    pass


class ScrubException(ZFSPoolException):
    """Raised when scrub operations fail"""
    pass


# Dataset-related exceptions
class ZFSDatasetException(ZFSException):
    """Base exception for ZFS dataset operations"""
    pass


class DatasetNotFoundException(ZFSDatasetException):
    """Raised when a specified dataset is not found"""
    pass


class DatasetAlreadyExistsException(ZFSDatasetException):
    """Raised when trying to create a dataset that already exists"""
    pass


class DatasetCreationException(ZFSDatasetException):
    """Raised when dataset creation fails"""
    pass


class DatasetDestructionException(ZFSDatasetException):
    """Raised when dataset destruction fails"""
    pass


class DatasetMountException(ZFSDatasetException):
    """Raised when dataset mount/unmount fails"""
    pass


class DatasetPropertyException(ZFSDatasetException):
    """Raised when setting/getting dataset properties fails"""
    pass


class DatasetRenameException(ZFSDatasetException):
    """Raised when dataset rename fails"""
    pass


# Snapshot-related exceptions
class ZFSSnapshotException(ZFSException):
    """Base exception for ZFS snapshot operations"""
    pass


class SnapshotNotFoundException(ZFSSnapshotException):
    """Raised when a specified snapshot is not found"""
    pass


class SnapshotAlreadyExistsException(ZFSSnapshotException):
    """Raised when trying to create a snapshot that already exists"""
    pass


class SnapshotCreationException(ZFSSnapshotException):
    """Raised when snapshot creation fails"""
    pass


class SnapshotDestructionException(ZFSSnapshotException):
    """Raised when snapshot destruction fails"""
    pass


class SnapshotRollbackException(ZFSSnapshotException):
    """Raised when snapshot rollback fails"""
    pass


class SnapshotCloneException(ZFSSnapshotException):
    """Raised when snapshot cloning fails"""
    pass


class SnapshotSendException(ZFSSnapshotException):
    """Raised when snapshot send operation fails"""
    pass


class SnapshotReceiveException(ZFSSnapshotException):
    """Raised when snapshot receive operation fails"""
    pass


class SnapshotHoldException(ZFSSnapshotException):
    """Raised when snapshot hold/release operations fail"""
    pass


# Replication-related exceptions
class ZFSReplicationException(ZFSException):
    """Base exception for ZFS replication operations"""
    pass


class ReplicationJobNotFoundException(ZFSReplicationException):
    """Raised when a replication job is not found"""
    pass


class ReplicationJobException(ZFSReplicationException):
    """Raised when replication job operations fail"""
    pass


class ReplicationExecutionException(ZFSReplicationException):
    """Raised when replication execution fails"""
    pass


class ReplicationConnectionException(ZFSReplicationException):
    """Raised when SSH connection for replication fails"""
    pass


class ReplicationTransferException(ZFSReplicationException):
    """Raised when data transfer during replication fails"""
    pass


# Observability-related exceptions
class ZFSObservabilityException(ZFSException):
    """Base exception for ZFS observability operations"""
    pass


class HistoryRetrievalException(ZFSObservabilityException):
    """Raised when pool history retrieval fails"""
    pass


class EventRetrievalException(ZFSObservabilityException):
    """Raised when pool event retrieval fails"""
    pass


class LogRetrievalException(ZFSObservabilityException):
    """Raised when log retrieval fails"""
    pass


class ARCStatsException(ZFSObservabilityException):
    """Raised when ARC statistics retrieval fails"""
    pass


class ModuleParameterException(ZFSObservabilityException):
    """Raised when module parameter operations fail"""
    pass


# Performance-related exceptions
class ZFSPerformanceException(ZFSException):
    """Base exception for ZFS performance monitoring"""
    pass


class IOStatException(ZFSPerformanceException):
    """Raised when iostat operations fail"""
    pass


class PerformanceMonitoringException(ZFSPerformanceException):
    """Raised when performance monitoring operations fail"""
    pass


class ProcessMonitoringException(ZFSPerformanceException):
    """Raised when process monitoring fails"""
    pass


# SMART-related exceptions
class SMARTException(Exception):
    """Base exception for SMART operations"""
    
    def __init__(self, message: str, disk: str = None):
        self.message = message
        self.disk = disk
        super().__init__(self.message)
    
    def __str__(self):
        if self.disk:
            return f"{self.message} (Disk: {self.disk})"
        return self.message


class SMARTNotAvailableException(SMARTException):
    """Raised when SMART is not available on a disk"""
    pass


class SMARTNotEnabledException(SMARTException):
    """Raised when SMART is not enabled on a disk"""
    pass


class SMARTDataRetrievalException(SMARTException):
    """Raised when SMART data retrieval fails"""
    pass


class SMARTTestException(SMARTException):
    """Raised when SMART test operations fail"""
    pass


class SMARTDaemonException(SMARTException):
    """Raised when smartd daemon operations fail"""
    pass


class SMARTConfigException(SMARTException):
    """Raised when smartd configuration operations fail"""
    pass


class DiskNotFoundException(SMARTException):
    """Raised when a disk is not found"""
    pass


# Permission exceptions
class PermissionException(ZFSException):
    """Raised when operation requires elevated privileges"""
    pass


class InsufficientPrivilegesException(PermissionException):
    """Raised when user lacks necessary privileges"""
    pass


# Validation exceptions
class ValidationException(Exception):
    """Base exception for validation errors"""
    pass


class InvalidPoolNameException(ValidationException):
    """Raised when pool name is invalid"""
    pass


class InvalidDatasetNameException(ValidationException):
    """Raised when dataset name is invalid"""
    pass


class InvalidSnapshotNameException(ValidationException):
    """Raised when snapshot name is invalid"""
    pass


class InvalidPropertyException(ValidationException):
    """Raised when property name or value is invalid"""
    pass


class InvalidScheduleException(ValidationException):
    """Raised when schedule expression is invalid"""
    pass


# System exceptions
class SystemException(Exception):
    """Base exception for system-level errors"""
    pass


class CommandNotFoundException(SystemException):
    """Raised when a required command is not found"""
    pass


class ZFSNotInstalledException(SystemException):
    """Raised when ZFS is not installed on the system"""
    pass


class SystemResourceException(SystemException):
    """Raised when system resources are insufficient"""
    pass


# Configuration exceptions
class ConfigurationException(Exception):
    """Base exception for configuration errors"""
    pass


class InvalidConfigurationException(ConfigurationException):
    """Raised when configuration is invalid"""
    pass


class MissingConfigurationException(ConfigurationException):
    """Raised when required configuration is missing"""
    pass
