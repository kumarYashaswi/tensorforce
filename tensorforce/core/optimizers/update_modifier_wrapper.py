# Copyright 2020 Tensorforce Team. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import tensorforce.core


def UpdateModifierWrapper(
    optimizer, *, multi_step=1, subsampling_fraction=1.0, clipping_threshold=None,
    optimizing_iterations=0, summary_labels=None, name=None, arguments_spec=None, **kwargs
):
    """
    Update modifier wrapper (specification key: `update_modifier_wrapper`).

    Args:
        optimizer (specification): Optimizer configuration
            (<span style="color:#C00000"><b>required</b></span>).
        multi_step (parameter, int > 0): Number of optimization steps
            (<span style="color:#00C000"><b>default</b></span>: single step).
        subsampling_fraction (parameter, 0.0 < float <= 1.0): Fraction of batch timesteps to
            subsample (<span style="color:#00C000"><b>default</b></span>: no subsampling).
        clipping_threshold (parameter, float > 0.0): Clipping threshold
            (<span style="color:#00C000"><b>default</b></span>: no clipping).
        optimizing_iterations (parameter, int >= 0):  Maximum number of line search iterations
            (<span style="color:#00C000"><b>default</b></span>: no optimizing).
        summary_labels ('all' | iter[string]): Labels of summaries to record
            (<span style="color:#00C000"><b>default</b></span>: inherit value of parent module).
        name (string): (<span style="color:#0000C0"><b>internal use</b></span>).
        arguments_spec (specification): <span style="color:#0000C0"><b>internal use</b></span>.
    """

    optimizer = dict(type=optimizer)
    optimizer.update(kwargs)
    if optimizing_iterations > 0:
        optimizer = dict(
            type='optimizing_step', optimizer=optimizer, ls_max_iterations=optimizing_iterations
        )
    if clipping_threshold is not None:
        optimizer = dict(type='clipping_step', optimizer=optimizer, threshold=clipping_threshold)
    if subsampling_fraction != 1.0:
        optimizer = dict(
            type='subsampling_step', optimizer=optimizer, fraction=subsampling_fraction
        )
    if multi_step > 1:
        optimizer = dict(type='multi_step', optimizer=optimizer, num_steps=multi_step)
    optimizer_cls = tensorforce.core.optimizer_modules[optimizer.pop('type')]

    return optimizer_cls(
        **optimizer, summary_labels=summary_labels, name=name, arguments_spec=arguments_spec
    )
