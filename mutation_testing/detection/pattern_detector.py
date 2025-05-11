import os

from mutation_testing.detection.pattern import PatternStatus
from mutation_testing.detection.utils import patterns_from_file, store_patterns_to_file
from mutation_testing.constants import DYNAMIC_PATTERN_FILENAME, STATIC_PATTERN_FILENAME


class PatternHandler:

    @staticmethod
    def get_static_patterns(static_analyzer, filename=STATIC_PATTERN_FILENAME):
        if static_analyzer:
            static_patterns = static_analyzer.static_patterns
        else:
            static_patterns = patterns_from_file(filename)[PatternStatus.STATIC]
        return static_patterns

    @staticmethod
    def get_dynamic_patterns(filename=DYNAMIC_PATTERN_FILENAME):
        patterns = patterns_from_file(filename)
        return patterns

    @staticmethod
    def get_categorized_patterns(static_analyzer=None, covered_lines=None) -> dict:
        patterns = PatternHandler.get_dynamic_patterns()
        static_patterns = PatternHandler.get_static_patterns(static_analyzer)
        uncovered_patterns = []
        equivalent_patterns = []
        if covered_lines:
            static_patterns, uncovered_patterns, equivalent_patterns = (
                PatternHandler.mark_uncovered_patterns(static_patterns, covered_lines))
        patterns[PatternStatus.STATIC] = static_patterns
        patterns[PatternStatus.UNCOVERED] = uncovered_patterns
        if PatternStatus.EQUIVALENT in patterns:
            patterns[PatternStatus.EQUIVALENT].extend(equivalent_patterns)
        else:
            patterns[PatternStatus.EQUIVALENT] = equivalent_patterns
        return patterns


    @staticmethod
    def get_patterns(static_analyzer=None, covered_lines=None):
        patterns = PatternHandler.get_categorized_patterns(static_analyzer, covered_lines)

        static_dynamic_patterns = []
        for pattern_status in patterns.keys():
            if pattern_status == PatternStatus.STATIC or pattern_status == PatternStatus.DYNAMIC:
                static_dynamic_patterns.extend(patterns[pattern_status])
        return (static_dynamic_patterns,
                patterns.get(PatternStatus.EQUIVALENT, []),
                patterns.get(PatternStatus.UNCOVERED, []))

    @staticmethod
    def mark_uncovered_patterns(static_patterns, covered_lines):
        uncovered_patterns = []
        refined_static_patterns = []
        equivalent_patterns = []

        for pattern in static_patterns:
            covered_lines_per_file = covered_lines.get(os.path.abspath(pattern.pattern_location.filename), [])
            if pattern.pattern_location.start_line not in covered_lines_per_file:
                pattern.pattern_status = PatternStatus.UNCOVERED
                uncovered_patterns.append(pattern)
            elif pattern.pattern_status == PatternStatus.EQUIVALENT:
                equivalent_patterns.append(pattern)
            else:
                refined_static_patterns.append(pattern)
        store_patterns_to_file(refined_static_patterns+uncovered_patterns+equivalent_patterns, STATIC_PATTERN_FILENAME, True)
        return refined_static_patterns, uncovered_patterns, equivalent_patterns
