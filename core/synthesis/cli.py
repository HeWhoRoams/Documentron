#!/usr/bin/env python3
"""
CLI entry point for Documentron doc synthesis.
"""

import argparse
import logging
import os
import sys
from pathlib import Path

# Import synthesis components
from Documentron.core.synthesis.artifact_loader import ArtifactLoader
from Documentron.core.synthesis.provenance import ProvenanceManager
from Documentron.artifacts.docs.doc_writer import DocWriter
from Documentron.artifacts.docs.overview import synthesize_overview
from Documentron.artifacts.docs.architecture import synthesize_architecture
from Documentron.artifacts.docs.api_reference import synthesize_api_reference
from Documentron.artifacts.docs.dependencies import synthesize_dependencies
from Documentron.artifacts.docs.maintenance_notes import synthesize_maintenance_notes

def check_positive_int(value):
    """Check that value is a positive integer."""
    try:
        ivalue = int(value)
        if ivalue <= 0:
            raise ValueError
        return ivalue
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not a positive integer")

def check_temperature(value):
    """Check that temperature is a float in [0, 2]."""
    try:
        fvalue = float(value)
        if not (0 <= fvalue <= 2):
            raise ValueError
        return fvalue
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not a float in range [0, 2]")

def check_non_negative_int(value):
    """Check that value is a non-negative integer."""
    try:
        ivalue = int(value)
        if ivalue < 0:
            raise ValueError
        return ivalue
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not a non-negative integer")

def synthesize_command(args):
    """Handle synthesize command"""
    logging.basicConfig(level=logging.INFO)
    
    artifacts_path = Path(args.artifacts)
    out_path = Path(args.out)
    
    # Validate artifacts path
    if not artifacts_path.exists():
        logging.error(f"Artifacts path does not exist: {artifacts_path}")
        return 1
    if not (artifacts_path.is_file() or artifacts_path.is_dir()):
        logging.error(f"Artifacts path is not a file or directory: {artifacts_path}")
        return 1
    if not artifacts_path.is_dir():
        logging.error(f"Artifacts path must be a directory: {artifacts_path}")
        return 1
    
    # Validate output path
    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        # Test write access
        test_file = out_path / ".test_write"
        test_file.write_text("test")
        test_file.unlink()
    except Exception as e:
        logging.error(f"Cannot write to output directory: {out_path} - {e}")
        return 1
    
    # Perform synthesis
    try:
        loader = ArtifactLoader(artifacts_path)
        artifacts = loader.load_artifacts()
        if not loader.validate_artifacts(artifacts):
            logging.error("Artifact validation failed")
            return 1

        # Generate provenance once for the run
        manager = ProvenanceManager()
        provenance = manager.generate_provenance(artifacts)

        # Ensure output directory exists
        out_path.mkdir(parents=True, exist_ok=True)

        # Write provenance snapshot for traceability
        try:
            import json as _json
            (out_path / "provenance.json").write_text(_json.dumps(provenance, indent=2), encoding="utf-8")
        except Exception:
            # Fall back to plain str if JSON serialization fails for any reason
            (out_path / "provenance.json").write_text(str(provenance), encoding="utf-8")

        # Synthesize each doc deterministically from artifacts
        writer = DocWriter(out_path)

        docs_to_generate = [
            ("overview", synthesize_overview),
            ("architecture", synthesize_architecture),
            ("api-reference", synthesize_api_reference),
            ("dependencies", synthesize_dependencies),
            ("maintenance-notes", synthesize_maintenance_notes),
        ]

        generated = 0
        for doc_type, synth_fn in docs_to_generate:
            try:
                content, citations = synth_fn(artifacts)
                # Optionally, we could add confidence signals here. Keep minimal/deterministic.
                writer.write_doc(doc_type, content, citations, provenance)
                generated += 1
            except Exception as e:
                logging.error(f"Failed to synthesize '{doc_type}': {e}")

        logging.info(f"Synthesis completed successfully. Generated {generated} docs in {out_path}")
        return 0
    except Exception as e:
        logging.error(f"Synthesis failed: {e}")
        return 1

def report_command(args):
    """Handle report command"""
    logging.basicConfig(level=logging.INFO)
    
    docs_path = Path(args.docs)
    artifacts_path = Path(args.artifacts)
    
    # Validate docs path
    if not os.path.exists(args.docs):
        logging.error(f"Docs path does not exist: {args.docs}")
        return 1
    if not os.access(args.docs, os.R_OK):
        logging.error(f"Docs path is not readable: {args.docs}")
        return 1
    if not docs_path.is_dir():
        logging.error(f"Docs path must be a directory: {args.docs}")
        return 1
    
    # Validate artifacts path
    if not os.path.exists(args.artifacts):
        logging.error(f"Artifacts path does not exist: {args.artifacts}")
        return 1
    if not os.access(args.artifacts, os.R_OK):
        logging.error(f"Artifacts path is not readable: {args.artifacts}")
        return 1
    if not artifacts_path.is_dir():
        logging.error(f"Artifacts path must be a directory: {args.artifacts}")
        return 1
    
    # Validate format
    supported_formats = ['md', 'json']
    if args.format not in supported_formats:
        logging.error(f"Unsupported format: {args.format}. Supported: {supported_formats}")
        return 1
    
    # Perform reporting
    try:
        loader = ArtifactLoader(artifacts_path)
        artifacts = loader.load_artifacts()
        if not loader.validate_artifacts(artifacts):
            logging.error("Artifact validation failed")
            return 1
        
        # TODO: Implement full reporting logic (load docs, generate coverage report, etc.)
        # For now, generate basic report
        manager = ProvenanceManager()
        provenance = manager.generate_provenance(artifacts)
        
        # Simple report
        report_content = f"# Report\n\nArtifacts loaded: {len(artifacts)}\nProvenance: {provenance}\n"
        
        if args.format == 'md':
            report_file = docs_path / "report.md"
            report_file.write_text(report_content, encoding="utf-8")
        elif args.format == 'json':
            import json
            report_file = docs_path / "report.json"
            report_file.write_text(json.dumps({"report": report_content}, indent=2), encoding="utf-8")
        
        logging.info(f"Report generated in {args.format} format at {report_file}")
        return 0
    except Exception as e:
        logging.error(f"Reporting failed: {e}")
        return 1

def main():
    parser = argparse.ArgumentParser(description="Documentron Doc Synthesis CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # synthesize command
    synth_parser = subparsers.add_parser('synthesize', help='Synthesize documentation from artifacts')
    synth_parser.add_argument('--artifacts', required=True, help='Path to artifacts directory')
    synth_parser.add_argument('--profile', default='default', help='Synthesis profile')
    synth_parser.add_argument('--out', required=True, help='Output directory for docs')
    synth_parser.add_argument('--max-docs', type=check_positive_int, default=6, help='Maximum number of docs')
    synth_parser.add_argument('--temperature', type=check_temperature, default=0.2, help='LLM temperature')
    synth_parser.add_argument('--seed', type=check_non_negative_int, default=42, help='Random seed')
    synth_parser.set_defaults(func=synthesize_command)

    # report command
    report_parser = subparsers.add_parser('report', help='Verify and report on synthesized docs')
    report_parser.add_argument('--artifacts', required=True, help='Path to artifacts directory')
    report_parser.add_argument('--docs', required=True, help='Path to docs directory')
    report_parser.add_argument('--format', default='md', help='Report format')
    report_parser.set_defaults(func=report_command)

    args = parser.parse_args()
    if args.command:
        return args.func(args)
    else:
        parser.print_help()
        return 1

if __name__ == '__main__':
    sys.exit(main())
