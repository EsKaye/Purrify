"""
Purrify Reporting Module

This module provides comprehensive reporting capabilities for
system optimization results and system status.
"""

import time
from typing import Dict, Any, Optional
from datetime import datetime
from loguru import logger

from ..core.config import Config
from ..utils.platform import format_bytes, get_system_info


class ReportGenerator:
    """
    Report generator for system optimization results.
    
    This class provides comprehensive reporting capabilities including
    markdown reports, JSON exports, and formatted summaries.
    """
    
    def __init__(self, config: Config):
        """
        Initialize the report generator.
        
        Args:
            config: Configuration object
        """
        self.config = config
        
        logger.info("ReportGenerator initialized")
    
    async def generate_report(
        self,
        scan_result: Optional[Any] = None,
        clean_result: Optional[Any] = None,
        optimization_result: Optional[Any] = None,
        detailed: bool = False
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive system optimization report.
        
        Args:
            scan_result: Results from system scan
            clean_result: Results from cleaning operation
            optimization_result: Results from optimization operation
            detailed: Include detailed information
            
        Returns:
            Dictionary containing report data
        """
        logger.info("Generating system optimization report...")
        
        try:
            # Get current system information
            system_info = get_system_info()
            
            # Generate report sections
            report_data = {
                "timestamp": datetime.now().isoformat(),
                "report_version": "1.0.0",
                "system_info": system_info,
                "summary": self._generate_summary(scan_result, clean_result, optimization_result),
                "markdown": self._generate_markdown_report(
                    scan_result, clean_result, optimization_result, system_info, detailed
                ),
                "json": self._generate_json_report(
                    scan_result, clean_result, optimization_result, system_info
                )
            }
            
            logger.info("Report generated successfully")
            return report_data
            
        except Exception as e:
            logger.error(f"Failed to generate report: {e}")
            return {"error": str(e)}
    
    def _generate_summary(
        self,
        scan_result: Optional[Any],
        clean_result: Optional[Any],
        optimization_result: Optional[Any]
    ) -> Dict[str, Any]:
        """Generate a summary of all operations."""
        summary = {
            "total_operations": 0,
            "total_space_freed": 0,
            "total_optimizations": 0,
            "overall_performance_improvement": 0.0
        }
        
        if scan_result:
            summary["total_operations"] += 1
            summary["potential_space_savings"] = getattr(scan_result, 'potential_space_savings', 0)
        
        if clean_result:
            summary["total_operations"] += 1
            summary["total_space_freed"] = getattr(clean_result, 'space_freed', 0)
            summary["files_cleaned"] = getattr(clean_result, 'files_cleaned', 0)
        
        if optimization_result:
            summary["total_operations"] += 1
            summary["total_optimizations"] = getattr(optimization_result, 'optimizations_applied', 0)
            summary["overall_performance_improvement"] = getattr(optimization_result, 'performance_improvement', 0.0)
        
        return summary
    
    def _generate_markdown_report(
        self,
        scan_result: Optional[Any],
        clean_result: Optional[Any],
        optimization_result: Optional[Any],
        system_info: Dict[str, Any],
        detailed: bool
    ) -> str:
        """Generate a markdown report."""
        report_lines = [
            "# 🐱 Purrify System Optimization Report",
            "",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Version:** 1.0.0",
            "",
            "## 📊 Executive Summary",
            ""
        ]
        
        # Add summary statistics
        if scan_result:
            report_lines.extend([
                f"- **Files Scanned:** {getattr(scan_result, 'total_files_scanned', 0):,}",
                f"- **Cache Files Found:** {getattr(scan_result, 'cache_files_found', 0):,}",
                f"- **Potential Space Savings:** {format_bytes(getattr(scan_result, 'potential_space_savings', 0))}",
                ""
            ])
        
        if clean_result:
            report_lines.extend([
                f"- **Files Cleaned:** {getattr(clean_result, 'files_cleaned', 0):,}",
                f"- **Space Freed:** {format_bytes(getattr(clean_result, 'space_freed', 0))}",
                f"- **Clean Duration:** {getattr(clean_result, 'clean_duration', 0):.2f}s",
                ""
            ])
        
        if optimization_result:
            report_lines.extend([
                f"- **Optimizations Applied:** {getattr(optimization_result, 'optimizations_applied', 0)}",
                f"- **Performance Improvement:** {getattr(optimization_result, 'performance_improvement', 0):.1f}%",
                f"- **Optimization Duration:** {getattr(optimization_result, 'optimization_duration', 0):.2f}s",
                ""
            ])
        
        # Add system information
        report_lines.extend([
            "## 🖥️ System Information",
            ""
        ])
        
        if "platform_type" in system_info:
            report_lines.append(f"- **Platform:** {system_info['platform_type']}")
        
        if "disk_usage" in system_info and "error" not in system_info["disk_usage"]:
            disk_info = system_info["disk_usage"]
            report_lines.extend([
                f"- **Total Disk Space:** {format_bytes(disk_info.get('total', 0))}",
                f"- **Used Disk Space:** {format_bytes(disk_info.get('used', 0))}",
                f"- **Free Disk Space:** {format_bytes(disk_info.get('free', 0))}",
                f"- **Disk Usage:** {disk_info.get('percent_used', 0):.1f}%",
                ""
            ])
        
        if "memory_info" in system_info and "error" not in system_info["memory_info"]:
            memory_info = system_info["memory_info"]
            report_lines.extend([
                f"- **Total Memory:** {format_bytes(memory_info.get('total', 0))}",
                f"- **Used Memory:** {format_bytes(memory_info.get('used', 0))}",
                f"- **Available Memory:** {format_bytes(memory_info.get('available', 0))}",
                f"- **Memory Usage:** {memory_info.get('percent_used', 0):.1f}%",
                ""
            ])
        
        # Add detailed sections if requested
        if detailed:
            if scan_result:
                report_lines.extend(self._generate_scan_details(scan_result))
            
            if clean_result:
                report_lines.extend(self._generate_clean_details(clean_result))
            
            if optimization_result:
                report_lines.extend(self._generate_optimization_details(optimization_result))
        
        # Add recommendations
        report_lines.extend([
            "## 💡 Recommendations",
            "",
            "### Immediate Actions",
            "- Run regular system scans to identify optimization opportunities",
            "- Clean browser caches weekly to maintain performance",
            "- Monitor startup items and disable unnecessary ones",
            "",
            "### Long-term Maintenance",
            "- Schedule regular system optimization sessions",
            "- Keep applications updated for optimal performance",
            "- Monitor disk space usage and clean up large files",
            "",
            "## 🔒 Safety Information",
            "",
            "- All operations are performed with safety checks",
            "- Critical system files are protected",
            "- Backups are created before major operations",
            "- AI-powered analysis ensures safe file handling",
            "",
            "---",
            "",
            "*Report generated by Purrify - AI-Driven System Optimization Utility*"
        ])
        
        return "\n".join(report_lines)
    
    def _generate_json_report(
        self,
        scan_result: Optional[Any],
        clean_result: Optional[Any],
        optimization_result: Optional[Any],
        system_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate a JSON report."""
        report = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "version": "1.0.0",
                "generator": "Purrify"
            },
            "system_info": system_info,
            "operations": {}
        }
        
        if scan_result:
            report["operations"]["scan"] = {
                "total_files_scanned": getattr(scan_result, 'total_files_scanned', 0),
                "cache_files_found": getattr(scan_result, 'cache_files_found', 0),
                "temp_files_found": getattr(scan_result, 'temp_files_found', 0),
                "log_files_found": getattr(scan_result, 'log_files_found', 0),
                "large_files_found": getattr(scan_result, 'large_files_found', 0),
                "potential_space_savings": getattr(scan_result, 'potential_space_savings', 0),
                "scan_duration": getattr(scan_result, 'scan_duration', 0),
                "scan_errors": getattr(scan_result, 'scan_errors', [])
            }
        
        if clean_result:
            report["operations"]["clean"] = {
                "files_cleaned": getattr(clean_result, 'files_cleaned', 0),
                "space_freed": getattr(clean_result, 'space_freed', 0),
                "clean_duration": getattr(clean_result, 'clean_duration', 0),
                "clean_errors": getattr(clean_result, 'clean_errors', []),
                "backup_created": getattr(clean_result, 'backup_created', False),
                "backup_path": getattr(clean_result, 'backup_path', None)
            }
        
        if optimization_result:
            report["operations"]["optimize"] = {
                "optimizations_applied": getattr(optimization_result, 'optimizations_applied', 0),
                "performance_improvement": getattr(optimization_result, 'performance_improvement', 0.0),
                "optimization_duration": getattr(optimization_result, 'optimization_duration', 0),
                "optimization_errors": getattr(optimization_result, 'optimization_errors', []),
                "startup_items_optimized": getattr(optimization_result, 'startup_items_optimized', 0),
                "memory_optimized": getattr(optimization_result, 'memory_optimized', False),
                "disk_optimized": getattr(optimization_result, 'disk_optimized', False)
            }
        
        return report
    
    def _generate_scan_details(self, scan_result: Any) -> list:
        """Generate detailed scan information."""
        lines = [
            "## 🔍 Scan Details",
            ""
        ]
        
        if hasattr(scan_result, 'file_details') and scan_result.file_details:
            lines.extend([
                "### File Categories",
                ""
            ])
            
            # Group files by category
            categories = {}
            for file_info in scan_result.file_details:
                category = file_info.get('category', 'unknown')
                if category not in categories:
                    categories[category] = []
                categories[category].append(file_info)
            
            for category, files in categories.items():
                total_size = sum(f.get('size', 0) for f in files)
                lines.extend([
                    f"#### {category.replace('_', ' ').title()}",
                    f"- **Files:** {len(files):,}",
                    f"- **Total Size:** {format_bytes(total_size)}",
                    ""
                ])
        
        return lines
    
    def _generate_clean_details(self, clean_result: Any) -> list:
        """Generate detailed cleaning information."""
        lines = [
            "## 🧹 Cleaning Details",
            ""
        ]
        
        if hasattr(clean_result, 'backup_created') and clean_result.backup_created:
            lines.extend([
                "### Backup Information",
                f"- **Backup Created:** ✅",
                f"- **Backup Location:** {getattr(clean_result, 'backup_path', 'Unknown')}",
                ""
            ])
        
        if hasattr(clean_result, 'clean_errors') and clean_result.clean_errors:
            lines.extend([
                "### Cleaning Errors",
                ""
            ])
            for error in clean_result.clean_errors:
                lines.append(f"- {error}")
            lines.append("")
        
        return lines
    
    def _generate_optimization_details(self, optimization_result: Any) -> list:
        """Generate detailed optimization information."""
        lines = [
            "## ⚡ Optimization Details",
            ""
        ]
        
        if hasattr(optimization_result, 'startup_items_optimized'):
            lines.extend([
                "### Startup Optimization",
                f"- **Startup Items Optimized:** {optimization_result.startup_items_optimized}",
                ""
            ])
        
        if hasattr(optimization_result, 'memory_optimized'):
            lines.extend([
                "### Memory Optimization",
                f"- **Memory Optimized:** {'✅' if optimization_result.memory_optimized else '❌'}",
                ""
            ])
        
        if hasattr(optimization_result, 'disk_optimized'):
            lines.extend([
                "### Disk Optimization",
                f"- **Disk Optimized:** {'✅' if optimization_result.disk_optimized else '❌'}",
                ""
            ])
        
        if hasattr(optimization_result, 'optimization_errors') and optimization_result.optimization_errors:
            lines.extend([
                "### Optimization Errors",
                ""
            ])
            for error in optimization_result.optimization_errors:
                lines.append(f"- {error}")
            lines.append("")
        
        return lines 