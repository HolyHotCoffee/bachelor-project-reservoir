# Notes


## Data
**Talk with Melih**
- The relation between N: Number of data points you train on, and
D (i dont know the name), and the number of parameters, does so
you do not overfit. If You have a lot of parameters, you can have
a lot of training data. He suggested to take all the training data.





Idea: Want to capture how will et perform in 

- Data consist of:
  - Good period
    - 20 days
    - 100 days
  - Bad period
      - 20 days prediction, Training 100 days
      - 100 days preidction, Training 800 days.


- 3rd Data:
  - Splitting training data up in smaller bites.
  To capture all the different trends. 



Training data on to much data: Will generate overfitting.
The model will fit to much to the training-model. 


Positive trend period: 2003 - 2007
Negative trend period: 2008 - 2012

### Keep in mind
- The robustness of the model. It may be affected by the changes,
in the market conditions (external factors that not capture.).
  - To account for this: 





## Analyzing



















## NotesReservoir 
size: The size of the reservoir layer is a critical hyperparameter in ESNs. A larger reservoir can potentially capture more complex patterns in the data, but it can also increase the risk of overfitting. On the other hand, a smaller reservoir may not capture enough of the underlying patterns in the data. You can experiment with different reservoir sizes to find the optimal size for your dataset.
Spectral radius: The spectral radius is another important hyperparameter that controls the dynamics of the reservoir layer. It determines the scaling of the recurrent weights and can affect the stability and performance of the network. In general, a larger spectral radius can increase the memory capacity of the network, but it can also lead to instability and overfitting. You can experiment with different spectral radii to find the optimal value for your dataset.
Sparsity: The sparsity of the recurrent weights is another hyperparameter that can affect the performance of ESNs. Sparsity refers to the percentage of zero weights in the recurrent weight matrix, and it can affect the amount of information that is propagated through the network. In general, a more sparse weight matrix can lead to better performance and generalization, but it can also increase the risk of underfitting. You can experiment with different levels of sparsity to find the optimal value for your dataset.
Input scaling: The scaling of the input weights is another hyperparameter that can affect the performance of ESNs. It determines how much influence the input has on the network dynamics and can affect the stability and performance of the network. In general, a larger input scaling can increase the sensitivity of the network to the input data, but it can also lead to instability and overfitting. You can experiment with different input scaling values to find the optimal value for your dataset.
Regularization: Regularization techniques such as ridge regression or Lasso can help to prevent overfitting and improve the generalization performance of ESNs. You can experiment with different regularization techniques and regularization strengths to find the optimal combination for your dataset.

warmup: parameter to set the amount of timesteps we want to discard at the beginning of train_states, when training.
  - Warmup, is update the networks ineternal state on the data. 
  - Once the warmup period is complete, the interal state of the network
  is assumed to have settled into a "good inital condition"
  - "Golden rule:" Set the warmup, so it caputeres the cycles.


## Advanced Features

&: Operator can be used to merge two model together.


forced_feedbacks: 
shift_fb: indicates forced feedback timeseries should be sshifted. 
warmup:

### Generation and Long term forecasting

reset: Reset internal state
We use the while loop, to use the prediction step, to be fed into the ESN again.
To generate the n timessteps prediction.

#### Deep architectures
>> chaining: allows to compose nodes to form a chain
&: Allows to merge models together, to create parallel pathways. 

#### Learning

Online training: Incremental
Offline training: Where the entire dataset is loaded into memory





#### Chatgpt #####
Ah, I see. In machine learning, 
the number of training data points is often denoted by N,
and the number of features (i.e., independent variables) is denoted by 
D. The number of parameters in a model can vary depending on 
the model architecture, 
but it generally refers to the number of weights or coefficients
that the model needs to learn from the data.

The relationship between N, D, and P can impact the
risk of overfitting in a model. As I mentioned earlier,
having a large number of parameters can increase the capacity 
of the model to fit the training data, which can increase 
the risk of overfitting. However, having a large amount of 
training data can help to regularize the model by 
providing more examples to learn from.

The general rule of thumb is that the number of 
training data points should be at least as 
large as the number of parameters in the model. 
In other words, N >= P. This helps to ensure that the
model has enough examples to learn from and reduces
the risk of overfitting. However, this rule is not a
hard and fast rule, and the appropriate number of
training data points can vary depending on
the complexity of the problem and the model architecture.

In summary, the relationship between N, D, 
and P can impact the risk of overfitting in a model. 
Having a large amount of
training data can help to regularize the model,
but the number of training data points
should be at least as large as the number
of parameters in the model.
